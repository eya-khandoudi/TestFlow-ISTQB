from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db
from app.services.istqb_engine import (
    validate_string_length,
    validate_risk_rating,
    calculate_risk,
    ISTQBValidationError
)

test_cases_bp = Blueprint('test_cases', __name__, url_prefix='/test-cases')

@test_cases_bp.route('/')
def list_test_cases():
    db = get_db()
    sort_by = request.args.get('sort', 'risk_desc')
    test_type = request.args.get('type')
    priority = request.args.get('priority')

    query = """
        SELECT tc.*, r.req_code, r.title as req_title
        FROM test_cases tc
        LEFT JOIN requirements r ON tc.requirement_id = r.id
        WHERE tc.project_id = 1
    """
    params = []

    if test_type:
        query += " AND tc.test_type = ?"
        params.append(test_type)
    if priority:
        query += " AND tc.priority = ?"
        params.append(priority)

    if sort_by == 'risk_desc':
        query += " ORDER BY risk_score DESC, tc.tc_code ASC"
    elif sort_by == 'code':
        query += " ORDER BY tc.tc_code ASC"
    elif sort_by == 'priority':
        query += " ORDER BY CASE tc.priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END"
    else:
        query += " ORDER BY tc.id DESC"

    tcs = db.execute(query, params).fetchall()

    # Enrich with risk info
    enriched_tcs = []
    for tc in tcs:
        d = dict(tc)
        risk = calculate_risk(d['risk_likelihood'], d['risk_impact'])
        d['risk_category'] = risk['category']
        d['risk_badge'] = risk['badge_class']
        enriched_tcs.append(d)

    return render_template('test_cases/list.html', test_cases=enriched_tcs, current_sort=sort_by)

@test_cases_bp.route('/<int:tc_id>')
def detail_test_case(tc_id):
    db = get_db()
    tc = db.execute("""
        SELECT tc.*, r.req_code, r.title as req_title
        FROM test_cases tc
        LEFT JOIN requirements r ON tc.requirement_id = r.id
        WHERE tc.id = ?
    """, (tc_id,)).fetchone()
    if not tc:
        flash("Test case not found.", "warning")
        return redirect(url_for('test_cases.list_test_cases'))

    risk = calculate_risk(tc['risk_likelihood'], tc['risk_impact'])
    executions = db.execute("""
        SELECT te.*, tr.run_code, tr.name as run_name
        FROM test_executions te
        JOIN test_runs tr ON te.test_run_id = tr.id
        WHERE te.test_case_id = ?
        ORDER BY te.executed_at DESC
    """, (tc_id,)).fetchall()

    defects = db.execute("SELECT * FROM defects WHERE test_case_id = ?", (tc_id,)).fetchall()

    return render_template(
        'test_cases/detail.html',
        tc=tc,
        risk=risk,
        executions=executions,
        defects=defects
    )

@test_cases_bp.route('/new', methods=['GET', 'POST'])
def create_test_case():
    db = get_db()
    reqs = db.execute("SELECT id, req_code, title FROM requirements ORDER BY req_code").fetchall()

    if request.method == 'POST':
        tc_code = request.form.get('tc_code', '').strip().upper()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        precondition = request.form.get('precondition', '').strip()
        steps = request.form.get('steps', '').strip()
        expected_result = request.form.get('expected_result', '').strip()
        test_type = request.form.get('test_type', 'Functional')
        priority = request.form.get('priority', 'Medium')
        req_id = request.form.get('requirement_id') or None
        likelihood = request.form.get('risk_likelihood', 2)
        impact = request.form.get('risk_impact', 3)

        try:
            # ISTQB BVA / EP Validations
            validate_string_length(tc_code, 3, 20, "Test Case Code")
            validate_string_length(title, 5, 200, "Title")
            validate_string_length(steps, 5, 2000, "Test Steps")
            validate_string_length(expected_result, 3, 1000, "Expected Result")
            l_val = validate_risk_rating(likelihood, "Risk Likelihood")
            i_val = validate_risk_rating(impact, "Risk Impact")

            db.execute("""
                INSERT INTO test_cases (
                    tc_code, title, description, precondition, steps, expected_result,
                    test_type, priority, risk_likelihood, risk_impact, requirement_id, project_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (tc_code, title, description, precondition, steps, expected_result, test_type, priority, l_val, i_val, req_id))
            db.commit()
            flash(f"Test Case {tc_code} successfully registered.", "success")
            return redirect(url_for('test_cases.list_test_cases'))
        except (ISTQBValidationError, Exception) as e:
            flash(str(e), "danger")

    return render_template('test_cases/form.html', tc=None, requirements=reqs)

@test_cases_bp.route('/<int:tc_id>/edit', methods=['GET', 'POST'])
def edit_test_case(tc_id):
    db = get_db()
    tc = db.execute("SELECT * FROM test_cases WHERE id = ?", (tc_id,)).fetchone()
    if not tc:
        flash("Test case not found.", "warning")
        return redirect(url_for('test_cases.list_test_cases'))

    reqs = db.execute("SELECT id, req_code, title FROM requirements ORDER BY req_code").fetchall()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        precondition = request.form.get('precondition', '').strip()
        steps = request.form.get('steps', '').strip()
        expected_result = request.form.get('expected_result', '').strip()
        test_type = request.form.get('test_type', 'Functional')
        priority = request.form.get('priority', 'Medium')
        req_id = request.form.get('requirement_id') or None
        likelihood = request.form.get('risk_likelihood', 2)
        impact = request.form.get('risk_impact', 3)

        try:
            validate_string_length(title, 5, 200, "Title")
            validate_string_length(steps, 5, 2000, "Test Steps")
            validate_string_length(expected_result, 3, 1000, "Expected Result")
            l_val = validate_risk_rating(likelihood, "Risk Likelihood")
            i_val = validate_risk_rating(impact, "Risk Impact")

            db.execute("""
                UPDATE test_cases
                SET title = ?, description = ?, precondition = ?, steps = ?, expected_result = ?,
                    test_type = ?, priority = ?, risk_likelihood = ?, risk_impact = ?, requirement_id = ?
                WHERE id = ?
            """, (title, description, precondition, steps, expected_result, test_type, priority, l_val, i_val, req_id, tc_id))
            db.commit()
            flash("Test Case updated successfully.", "success")
            return redirect(url_for('test_cases.detail_test_case', tc_id=tc_id))
        except (ISTQBValidationError, Exception) as e:
            flash(str(e), "danger")

    return render_template('test_cases/form.html', tc=tc, requirements=reqs)

@test_cases_bp.route('/<int:tc_id>/delete', methods=['POST'])
def delete_test_case(tc_id):
    db = get_db()
    db.execute("DELETE FROM test_cases WHERE id = ?", (tc_id,))
    db.commit()
    flash("Test Case deleted.", "info")
    return redirect(url_for('test_cases.list_test_cases'))
