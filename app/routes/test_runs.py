from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import get_db
import datetime

test_runs_bp = Blueprint('test_runs', __name__, url_prefix='/test-runs')

@test_runs_bp.route('/')
def list_test_runs():
    db = get_db()
    runs = db.execute("""
        SELECT tr.*, 
            COUNT(te.id) as total_tests,
            SUM(CASE WHEN te.status = 'Pass' THEN 1 ELSE 0 END) as passed_tests,
            SUM(CASE WHEN te.status = 'Fail' THEN 1 ELSE 0 END) as failed_tests,
            SUM(CASE WHEN te.status = 'Blocked' THEN 1 ELSE 0 END) as blocked_tests
        FROM test_runs tr
        LEFT JOIN test_executions te ON tr.id = te.test_run_id
        WHERE tr.project_id = 1
        GROUP BY tr.id
        ORDER BY tr.created_at DESC
    """).fetchall()
    return render_template('test_runs/list.html', runs=runs)

@test_runs_bp.route('/new', methods=['GET', 'POST'])
def create_test_run():
    db = get_db()
    if request.method == 'POST':
        run_code = request.form.get('run_code', '').strip().upper()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        environment = request.form.get('environment', 'QA')

        if not run_code or not name:
            flash("Run code and Name are required.", "danger")
        else:
            try:
                cur = db.execute("""
                    INSERT INTO test_runs (run_code, name, description, environment, status, project_id)
                    VALUES (?, ?, ?, ?, 'In Progress', 1)
                """, (run_code, name, description, environment))
                run_id = cur.lastrowid

                # Auto-populate all existing test cases for this run
                tcs = db.execute("SELECT id FROM test_cases WHERE project_id = 1").fetchall()
                for tc in tcs:
                    db.execute("""
                        INSERT INTO test_executions (test_run_id, test_case_id, status)
                        VALUES (?, ?, 'Untested')
                    """, (run_id, tc['id']))
                db.commit()
                flash(f"Test Run {run_code} initialized with {len(tcs)} test cases.", "success")
                return redirect(url_for('test_runs.detail_test_run', run_id=run_id))
            except Exception as e:
                flash(f"Error creating test run: {str(e)}", "danger")

    return render_template('test_runs/form.html')

@test_runs_bp.route('/<int:run_id>')
def detail_test_run(run_id):
    db = get_db()
    run = db.execute("SELECT * FROM test_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        flash("Test Run not found.", "warning")
        return redirect(url_for('test_runs.list_test_runs'))

    executions = db.execute("""
        SELECT te.*, tc.tc_code, tc.title as tc_title, tc.priority as tc_priority,
               tc.test_type, (tc.risk_likelihood * tc.risk_impact) as risk_score,
               d.id as defect_id, d.bug_code, d.status as defect_status
        FROM test_executions te
        JOIN test_cases tc ON te.test_case_id = tc.id
        LEFT JOIN defects d ON te.id = d.test_execution_id
        WHERE te.test_run_id = ?
        ORDER BY tc.risk_score DESC, tc.tc_code ASC
    """, (run_id,)).fetchall()

    total = len(executions)
    passed = sum(1 for e in executions if e['status'] == 'Pass')
    failed = sum(1 for e in executions if e['status'] == 'Fail')
    blocked = sum(1 for e in executions if e['status'] == 'Blocked')
    untested = sum(1 for e in executions if e['status'] in ('Untested', 'Skipped'))
    pass_rate = round((passed / total * 100), 1) if total > 0 else 0.0

    return render_template(
        'test_runs/detail.html',
        run=run,
        executions=executions,
        total=total,
        passed=passed,
        failed=failed,
        blocked=blocked,
        untested=untested,
        pass_rate=pass_rate
    )

@test_runs_bp.route('/<int:run_id>/execute/<int:tc_id>', methods=['POST'])
def execute_test(run_id, tc_id):
    db = get_db()
    status = request.form.get('status', 'Pass')
    actual_result = request.form.get('actual_result', '').strip()
    notes = request.form.get('notes', '').strip()
    executed_by = request.form.get('executed_by', 'QA Engineer').strip()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.execute("""
        UPDATE test_executions
        SET status = ?, actual_result = ?, notes = ?, executed_by = ?, executed_at = ?
        WHERE test_run_id = ? AND test_case_id = ?
    """, (status, actual_result, notes, executed_by, now_str, run_id, tc_id))
    db.commit()

    flash(f"Test case execution recorded as '{status}'.", "success")
    return redirect(url_for('test_runs.detail_test_run', run_id=run_id))
