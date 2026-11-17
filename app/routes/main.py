from flask import Blueprint, render_template, abort
from app.services.report_service import get_dashboard_metrics, get_traceability_matrix, get_test_summary_report
from app.database import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    metrics = get_dashboard_metrics(project_id=1)
    db = get_db()
    project = db.execute("SELECT * FROM projects WHERE id = 1").fetchone()
    recent_defects = db.execute("""
        SELECT * FROM defects ORDER BY created_at DESC LIMIT 5
    """).fetchall()
    active_runs = db.execute("""
        SELECT * FROM test_runs WHERE project_id = 1 ORDER BY created_at DESC LIMIT 3
    """).fetchall()
    return render_template(
        'dashboard.html',
        metrics=metrics,
        project=project,
        recent_defects=recent_defects,
        active_runs=active_runs
    )

@main_bp.route('/rtm')
def traceability_matrix():
    rtm_data = get_traceability_matrix(project_id=1)
    return render_template('reports/rtm.html', rtm=rtm_data)

@main_bp.route('/report/<int:run_id>')
def test_summary_report(run_id):
    report_data = get_test_summary_report(run_id)
    if not report_data:
        abort(404, "Test Run not found")
    return render_template('reports/test_summary_report.html', **report_data)

@main_bp.route('/istqb-guide')
def istqb_guide():
    return render_template('reports/istqb_guide.html')
