from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db
from app.services.istqb_engine import (
    validate_defect_transition,
    get_allowed_transitions,
    triage_defect_decision_table,
    validate_string_length,
    InvalidStateTransitionError,
    ISTQBValidationError
)
import datetime

defects_bp = Blueprint('defects', __name__, url_prefix='/defects')

@defects_bp.route('/')
def list_defects():
    db = get_db()
    status_filter = request.args.get('status')
    severity_filter = request.args.get('severity')

    query = """
        SELECT d.*, tc.tc_code, tc.title as tc_title
        FROM defects d
        LEFT JOIN test_cases tc ON d.test_case_id = tc.id
        WHERE 1=1
    """
    params = []
    if status_filter:
        query += " AND d.status = ?"
        params.append(status_filter)
    if severity_filter:
        query += " AND d.severity = ?"
        params.append(severity_filter)

    query += " ORDER BY d.created_at DESC"
    defects = db.execute(query, params).fetchall()

    return render_template('defects/list.html', defects=defects, current_status=status_filter, current_severity=severity_filter)

@defects_bp.route('/new', methods=['GET', 'POST'])
def create_defect():
    db = get_db()
    tcs = db.execute("SELECT id, tc_code, title FROM test_cases ORDER BY tc_code").fetchall()
    runs = db.execute("SELECT id, run_code, name FROM test_runs ORDER BY id DESC").fetchall()

    tc_id_prefill = request.args.get('tc_id')
    run_id_prefill = request.args.get('run_id')

    if request.method == 'POST':
        bug_code = request.form.get('bug_code', '').strip().upper()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        steps_to_reproduce = request.form.get('steps_to_reproduce', '').strip()
        severity = request.form.get('severity', 'Major')
        environment = request.form.get('environment', 'QA')
        assigned_to = request.form.get('assigned_to', 'Unassigned').strip()
        tc_id = request.form.get('test_case_id') or None
        run_id = request.form.get('test_run_id') or None

        # Check Decision Table Auto-triage
        is_core = bool(request.form.get('is_core_flow'))
        triage = triage_defect_decision_table(severity, environment, is_core)
        priority = request.form.get('priority') or triage['priority']

        try:
            validate_string_length(bug_code, 3, 20, "Defect Code")
            validate_string_length(title, 5, 200, "Title")
            validate_string_length(steps_to_reproduce, 5, 2000, "Steps to Reproduce")

            # Find matching test_execution_id if both tc_id and run_id provided
            exec_id = None
            if tc_id and run_id:
                ex_row = db.execute("""
                    SELECT id FROM test_executions WHERE test_run_id = ? AND test_case_id = ?
                """, (run_id, tc_id)).fetchone()
                if ex_row:
                    exec_id = ex_row['id']

            cur = db.execute("""
                INSERT INTO defects (
                    bug_code, title, description, steps_to_reproduce, severity, priority,
                    status, environment, test_case_id, test_execution_id, assigned_to
                ) VALUES (?, ?, ?, ?, ?, ?, 'New', ?, ?, ?, ?)
            """, (bug_code, title, description, steps_to_reproduce, severity, priority, environment, tc_id, exec_id, assigned_to))
            defect_id = cur.lastrowid

            # Initial history record
            db.execute("""
                INSERT INTO defect_history (defect_id, from_status, to_status, changed_by, comment)
                VALUES (?, 'None', 'New', 'QA Engineer', 'Defect logged and submitted.')
            """, (defect_id,))

            db.commit()
            flash(f"Defect {bug_code} logged successfully in state 'New'.", "success")
            return redirect(url_for('defects.detail_defect', defect_id=defect_id))
        except (ISTQBValidationError, Exception) as e:
            flash(str(e), "danger")

    return render_template(
        'defects/form.html',
        test_cases=tcs,
        test_runs=runs,
        tc_id_prefill=tc_id_prefill,
        run_id_prefill=run_id_prefill
    )

@defects_bp.route('/<int:defect_id>')
def detail_defect(defect_id):
    db = get_db()
    defect = db.execute("""
        SELECT d.*, tc.tc_code, tc.title as tc_title
        FROM defects d
        LEFT JOIN test_cases tc ON d.test_case_id = tc.id
        WHERE d.id = ?
    """, (defect_id,)).fetchone()
    if not defect:
        flash("Defect not found.", "warning")
        return redirect(url_for('defects.list_defects'))

    allowed_transitions = get_allowed_transitions(defect['status'])
    history = db.execute("""
        SELECT * FROM defect_history WHERE defect_id = ? ORDER BY changed_at DESC
    """, (defect_id,)).fetchall()

    return render_template(
        'defects/detail.html',
        defect=defect,
        allowed_transitions=allowed_transitions,
        history=history
    )

@defects_bp.route('/<int:defect_id>/transition', methods=['POST'])
def transition_defect(defect_id):
    db = get_db()
    defect = db.execute("SELECT * FROM defects WHERE id = ?", (defect_id,)).fetchone()
    if not defect:
        flash("Defect not found.", "danger")
        return redirect(url_for('defects.list_defects'))

    new_status = request.form.get('new_status')
    notes = request.form.get('notes', '').strip()
    changed_by = request.form.get('changed_by', 'QA Lead').strip()

    try:
        # Validate through the ISTQB Defect Lifecycle State Machine
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
        """, (defect_id, defect['status'], new_status, changed_by, notes or f"Transitioned to {new_status}"))

        db.commit()
        flash(f"State transition successful: {defect['status']} -> {new_status}", "success")
    except InvalidStateTransitionError as e:
        flash(f"ISTQB State Transition Violation: {str(e)}", "danger")

    return redirect(url_for('defects.detail_defect', defect_id=defect_id))
