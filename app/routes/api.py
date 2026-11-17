from flask import Blueprint, jsonify, request
from app.database import get_db
from app.services.report_service import get_dashboard_metrics, get_traceability_matrix
from app.services.istqb_engine import (
    validate_defect_transition,
    triage_defect_decision_table,
    calculate_risk,
    validate_cart_quantity,
    validate_string_length,
    validate_risk_rating,
    InvalidStateTransitionError,
    ISTQBValidationError
)
import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "TestFlow ISTQB Test Management System",
        "timestamp": datetime.datetime.now().isoformat()
    })

@api_bp.route('/metrics', methods=['GET'])
def metrics():
    m = get_dashboard_metrics(project_id=1)
    return jsonify(m)

@api_bp.route('/requirements', methods=['GET'])
def get_requirements():
    db = get_db()
    rows = db.execute("SELECT * FROM requirements ORDER BY req_code").fetchall()
    return jsonify([dict(r) for r in rows])

@api_bp.route('/test-cases', methods=['GET', 'POST'])
def test_cases():
    db = get_db()
    if request.method == 'GET':
        rows = db.execute("SELECT * FROM test_cases ORDER BY tc_code").fetchall()
        return jsonify([dict(r) for r in rows])

    # POST: create test case with BVA and EP validation
    data = request.get_json() or {}
    try:
        tc_code = validate_string_length(data.get('tc_code', ''), 3, 20, "Test Case Code")
        title = validate_string_length(data.get('title', ''), 5, 200, "Title")
        steps = validate_string_length(data.get('steps', ''), 5, 2000, "Steps")
        expected = validate_string_length(data.get('expected_result', ''), 3, 1000, "Expected Result")
        likelihood = validate_risk_rating(data.get('risk_likelihood', 2), "Risk Likelihood")
        impact = validate_risk_rating(data.get('risk_impact', 3), "Risk Impact")

        cur = db.execute("""
            INSERT INTO test_cases (
                tc_code, title, description, precondition, steps, expected_result,
                test_type, priority, risk_likelihood, risk_impact, requirement_id, project_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            tc_code, title, data.get('description', ''), data.get('precondition', ''),
            steps, expected, data.get('test_type', 'Functional'), data.get('priority', 'Medium'),
            likelihood, impact, data.get('requirement_id')
        ))
        db.commit()
        return jsonify({"id": cur.lastrowid, "tc_code": tc_code, "status": "created"}), 201
    except (ISTQBValidationError, Exception) as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/test-runs/<int:run_id>/executions', methods=['POST'])
def record_execution(run_id):
    db = get_db()
    data = request.get_json() or {}
    tc_id = data.get('test_case_id')
    status = data.get('status', 'Pass')
    actual = data.get('actual_result', '')
    executed_by = data.get('executed_by', 'API Automation')
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not tc_id:
        return jsonify({"error": "test_case_id is required"}), 400

    db.execute("""
        UPDATE test_executions
        SET status = ?, actual_result = ?, executed_by = ?, executed_at = ?
        WHERE test_run_id = ? AND test_case_id = ?
    """, (status, actual, executed_by, now_str, run_id, tc_id))
    db.commit()
    return jsonify({"run_id": run_id, "test_case_id": tc_id, "status": status, "updated_at": now_str})

@api_bp.route('/defects', methods=['GET', 'POST'])
def defects_api():
    db = get_db()
    if request.method == 'GET':
        rows = db.execute("SELECT * FROM defects ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows])

    data = request.get_json() or {}
    try:
        bug_code = validate_string_length(data.get('bug_code', ''), 3, 20, "Bug Code")
        title = validate_string_length(data.get('title', ''), 5, 200, "Title")
        steps = validate_string_length(data.get('steps_to_reproduce', ''), 5, 2000, "Steps")

        cur = db.execute("""
            INSERT INTO defects (
                bug_code, title, description, steps_to_reproduce, severity, priority,
                status, environment, test_case_id, assigned_to
            ) VALUES (?, ?, ?, ?, ?, ?, 'New', ?, ?, ?)
        """, (
            bug_code, title, data.get('description', ''), steps,
            data.get('severity', 'Major'), data.get('priority', 'Medium'),
            data.get('environment', 'QA'), data.get('test_case_id'),
            data.get('assigned_to', 'Unassigned')
        ))
        defect_id = cur.lastrowid
        db.execute("""
            INSERT INTO defect_history (defect_id, from_status, to_status, changed_by, comment)
            VALUES (?, 'None', 'New', 'API', 'Created via API')
        """, (defect_id,))
        db.commit()
        return jsonify({"id": defect_id, "bug_code": bug_code, "status": "New"}), 201
    except (ISTQBValidationError, Exception) as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/defects/<int:defect_id>/transition', methods=['POST'])
def transition_api(defect_id):
    db = get_db()
    defect = db.execute("SELECT * FROM defects WHERE id = ?", (defect_id,)).fetchone()
    if not defect:
        return jsonify({"error": "Defect not found"}), 404

    data = request.get_json() or {}
    new_status = data.get('new_status')
    notes = data.get('notes', '')
    changed_by = data.get('changed_by', 'API Tester')

    try:
        validate_defect_transition(defect['status'], new_status, notes=notes)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.execute("""
            UPDATE defects 
            SET status = ?, resolution_notes = CASE WHEN ? != '' THEN ? ELSE resolution_notes END, updated_at = ?
            WHERE id = ?
        """, (new_status, notes, notes, now_str, defect_id))

        db.execute("""
            INSERT INTO defect_history (defect_id, from_status, to_status, changed_by, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (defect_id, defect['status'], new_status, changed_by, notes))
        db.commit()

        return jsonify({
            "defect_id": defect_id,
            "previous_status": defect['status'],
            "new_status": new_status,
            "status": "transition_successful"
        })
    except InvalidStateTransitionError as e:
        return jsonify({"error": "InvalidStateTransitionError", "message": str(e)}), 422

# ==============================================================================
# ISTQB HELPER API ENDPOINTS (FOR AUTOMATED ISTQB TECHNIQUE TESTING)
# ==============================================================================
@api_bp.route('/istqb/triage', methods=['POST'])
def triage_evaluation():
    data = request.get_json() or {}
    sev = data.get('severity', 'Major')
    env = data.get('environment', 'QA')
    core = bool(data.get('is_core_flow', False))
    result = triage_defect_decision_table(sev, env, core)
    return jsonify(result)

@api_bp.route('/istqb/risk', methods=['POST'])
def risk_evaluation():
    data = request.get_json() or {}
    try:
        l = data.get('likelihood')
        i = data.get('impact')
        result = calculate_risk(l, i)
        return jsonify(result)
    except ISTQBValidationError as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/istqb/validate-cart', methods=['POST'])
def cart_bva_evaluation():
    data = request.get_json() or {}
    try:
        qty = data.get('quantity')
        valid_qty = validate_cart_quantity(qty)
        return jsonify({"quantity": valid_qty, "status": "valid"})
    except ISTQBValidationError as e:
        return jsonify({"error": str(e), "status": "invalid"}), 400
