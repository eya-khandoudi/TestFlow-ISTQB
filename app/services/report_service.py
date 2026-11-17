"""
Reporting Service:
Generates Dashboard metrics, Requirements Traceability Matrix (RTM),
and IEEE 829 compliant Test Summary Reports.
"""
from app.database import get_db
from app.services.istqb_engine import evaluate_release_gate

def get_dashboard_metrics(project_id: int = 1):
    db = get_db()

    # Total counts
    tc_count = db.execute("SELECT COUNT(*) FROM test_cases WHERE project_id = ?", (project_id,)).fetchone()[0]
    req_count = db.execute("SELECT COUNT(*) FROM requirements WHERE project_id = ?", (project_id,)).fetchone()[0]
    run_count = db.execute("SELECT COUNT(*) FROM test_runs WHERE project_id = ?", (project_id,)).fetchone()[0]
    defect_count = db.execute("SELECT COUNT(*) FROM defects").fetchone()[0]

    # Execution status breakdown
    exec_stats = db.execute("""
        SELECT status, COUNT(*) as count 
        FROM test_executions 
        GROUP BY status
    """).fetchall()
    exec_map = {row['status']: row['count'] for row in exec_stats}

    total_exec = sum(exec_map.values()) or 0
    passed = exec_map.get('Pass', 0)
    failed = exec_map.get('Fail', 0)
    blocked = exec_map.get('Blocked', 0)
    untested = exec_map.get('Untested', 0) + exec_map.get('Skipped', 0)

    pass_rate = (passed / total_exec * 100) if total_exec > 0 else 0.0

    # Defect severity breakdown
    defect_sev_rows = db.execute("""
        SELECT severity, COUNT(*) as count 
        FROM defects 
        GROUP BY severity
    """).fetchall()
    defect_sev = {row['severity']: row['count'] for row in defect_sev_rows}

    # Defect status breakdown
    defect_status_rows = db.execute("""
        SELECT status, COUNT(*) as count 
        FROM defects 
        GROUP BY status
    """).fetchall()
    defect_status = {row['status']: row['count'] for row in defect_status_rows}

    # Open Blocker / Critical defects count
    open_blockers = db.execute("""
        SELECT COUNT(*) FROM defects 
        WHERE severity IN ('Blocker', 'Critical') 
        AND status NOT IN ('Closed', 'Rejected')
    """).fetchone()[0]

    # Critical tests pass check
    critical_tests = db.execute("""
        SELECT tc.id, COALESCE(te.status, 'Untested') as exec_status
        FROM test_cases tc
        LEFT JOIN test_executions te ON tc.id = te.test_case_id
        WHERE tc.priority = 'Critical' AND tc.project_id = ?
    """, (project_id,)).fetchall()
    
    critical_passed = all(row['exec_status'] == 'Pass' for row in critical_tests) if critical_tests else True

    # Release Gate evaluation using ISTQB Decision Table
    gate = evaluate_release_gate(open_blockers, pass_rate, critical_passed)

    # Risk Distribution
    risk_rows = db.execute("""
        SELECT 
            CASE 
                WHEN (risk_likelihood * risk_impact) >= 16 THEN 'Critical'
                WHEN (risk_likelihood * risk_impact) >= 10 THEN 'High'
                WHEN (risk_likelihood * risk_impact) >= 5  THEN 'Medium'
                ELSE 'Low'
            END as risk_level,
            COUNT(*) as count
        FROM test_cases
        WHERE project_id = ?
        GROUP BY risk_level
    """, (project_id,)).fetchall()
    risk_dist = {row['risk_level']: row['count'] for row in risk_rows}

    return {
        "tc_count": tc_count,
        "req_count": req_count,
        "run_count": run_count,
        "defect_count": defect_count,
        "total_executions": total_exec,
        "passed": passed,
        "failed": failed,
        "blocked": blocked,
        "untested": untested,
        "pass_rate": round(pass_rate, 1),
        "open_blockers": open_blockers,
        "exec_map": exec_map,
        "defect_sev": defect_sev,
        "defect_status": defect_status,
        "risk_dist": risk_dist,
        "release_gate": gate
    }

def get_traceability_matrix(project_id: int = 1):
    """
    Builds the complete Requirements Traceability Matrix (RTM):
    Requirement -> Test Case -> Test Execution -> Defect
    Enables forward and backward traceability validation.
    """
    db = get_db()
    sql = """
        SELECT 
            r.id as req_id,
            r.req_code,
            r.title as req_title,
            r.priority as req_priority,
            tc.id as tc_id,
            tc.tc_code,
            tc.title as tc_title,
            tc.priority as tc_priority,
            (tc.risk_likelihood * tc.risk_impact) as risk_score,
            te.id as exec_id,
            te.status as exec_status,
            te.executed_by,
            d.id as defect_id,
            d.bug_code,
            d.title as bug_title,
            d.severity as bug_severity,
            d.status as bug_status
        FROM requirements r
        LEFT JOIN test_cases tc ON r.id = tc.requirement_id
        LEFT JOIN test_executions te ON tc.id = te.test_case_id
        LEFT JOIN defects d ON (tc.id = d.test_case_id OR te.id = d.test_execution_id OR r.id = d.requirement_id)
        WHERE r.project_id = ?
        ORDER BY r.req_code, tc.tc_code
    """
    rows = db.execute(sql, (project_id,)).fetchall()

    # Also detect orphaned test cases (test cases without linked requirements)
    orphaned_tcs = db.execute("""
        SELECT tc_code, title 
        FROM test_cases 
        WHERE requirement_id IS NULL AND project_id = ?
    """, (project_id,)).fetchall()

    # Calculate RTM Coverage Metrics
    total_reqs = db.execute("SELECT COUNT(*) FROM requirements WHERE project_id = ?", (project_id,)).fetchone()[0]
    covered_reqs = db.execute("""
        SELECT COUNT(DISTINCT requirement_id) 
        FROM test_cases 
        WHERE requirement_id IS NOT NULL AND project_id = ?
    """, (project_id,)).fetchone()[0]

    coverage_pct = (covered_reqs / total_reqs * 100) if total_reqs > 0 else 0.0

    return {
        "rows": rows,
        "orphaned_tcs": orphaned_tcs,
        "total_requirements": total_reqs,
        "covered_requirements": covered_reqs,
        "coverage_percentage": round(coverage_pct, 1)
    }

def get_test_summary_report(run_id: int = 1):
    """
    Generates a structured IEEE 829 / ISTQB Test Summary Report.
    Includes:
    - Test Summary Identifier & Scope
    - Variances & Incidents Summary
    - Comprehensive Assessment against Exit Criteria
    - Approvals and Sign-off recommendation
    """
    db = get_db()
    run = db.execute("SELECT * FROM test_runs WHERE id = ?", (run_id,)).fetchone()
    if not run:
        return None

    project = db.execute("SELECT * FROM projects WHERE id = ?", (run['project_id'],)).fetchone()
    executions = db.execute("""
        SELECT te.*, tc.tc_code, tc.title as tc_title, tc.priority as tc_priority,
               (tc.risk_likelihood * tc.risk_impact) as risk_score,
               d.bug_code, d.severity as bug_severity, d.status as bug_status
        FROM test_executions te
        JOIN test_cases tc ON te.test_case_id = tc.id
        LEFT JOIN defects d ON te.id = d.test_execution_id
        WHERE te.test_run_id = ?
        ORDER BY tc.tc_code
    """, (run_id,)).fetchall()

    total = len(executions)
    passed = sum(1 for e in executions if e['status'] == 'Pass')
    failed = sum(1 for e in executions if e['status'] == 'Fail')
    blocked = sum(1 for e in executions if e['status'] == 'Blocked')
    untested = sum(1 for e in executions if e['status'] in ('Untested', 'Skipped'))
    pass_rate = (passed / total * 100) if total > 0 else 0.0

    defects = db.execute("""
        SELECT * FROM defects 
        WHERE test_execution_id IN (SELECT id FROM test_executions WHERE test_run_id = ?)
    """, (run_id,)).fetchall()

    open_blockers = sum(1 for d in defects if d['severity'] in ('Blocker', 'Critical') and d['status'] not in ('Closed', 'Rejected'))
    critical_tests_passed = all(e['status'] == 'Pass' for e in executions if e['tc_priority'] == 'Critical')

    gate = evaluate_release_gate(open_blockers, pass_rate, critical_tests_passed)

    return {
        "run": run,
        "project": project,
        "executions": executions,
        "total": total,
        "passed": passed,
        "failed": failed,
        "blocked": blocked,
        "untested": untested,
        "pass_rate": round(pass_rate, 1),
        "defects": defects,
        "open_blockers": open_blockers,
        "gate": gate
    }
