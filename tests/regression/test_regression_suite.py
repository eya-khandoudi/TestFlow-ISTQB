"""
ISTQB Test Technique: Regression Testing
Ensures that code modifications, bug fixes, or enhancements do not introduce
new defects into existing functionality.
Simulates a complete End-to-End STLC cycle.
"""
import pytest
from app.services.report_service import get_traceability_matrix, get_test_summary_report

@pytest.mark.regression
class TestRegressionSuite:

    def test_e2e_stlc_regression_cycle(self, client, db):
        """
        Full End-to-End STLC regression test:
        1. Create Requirement
        2. Create Test Case with BVA & RBT assessment
        3. Create Test Run & Execute
        4. Log Defect on Failure
        5. Progress Defect through ISTQB State Machine to 'Closed'
        6. Validate RTM Traceability and IEEE 829 Test Summary Report
        """
        # Step 1: Create Requirement
        req_resp = client.post('/requirements/new', data={
            "req_code": "REQ-REG-99",
            "title": "One-Click Instant Checkout Support",
            "category": "Functional",
            "priority": "High",
            "description": "User can checkout in 1 click using saved default payment and address."
        }, follow_redirects=True)
        assert req_resp.status_code == 200

        req_row = db.execute("SELECT id FROM requirements WHERE req_code = 'REQ-REG-99'").fetchone()
        assert req_row is not None
        req_id = req_row['id']

        # Step 2: Create Test Case linked to Requirement
        tc_resp = client.post('/test-cases/new', data={
            "tc_code": "TC-REG-099",
            "title": "Verify One-Click Checkout with Saved Visa",
            "requirement_id": req_id,
            "test_type": "Regression",
            "priority": "High",
            "risk_likelihood": 3,
            "risk_impact": 4,
            "precondition": "Default card saved in profile.",
            "steps": "1. Click Instant Checkout button\n2. Verify order placed",
            "expected_result": "Order confirmation modal appears"
        }, follow_redirects=True)
        assert tc_resp.status_code == 200

        tc_row = db.execute("SELECT id FROM test_cases WHERE tc_code = 'TC-REG-099'").fetchone()
        assert tc_row is not None
        tc_id = tc_row['id']

        # Step 3: Initialize Test Run & Record Failed Execution
        run_resp = client.post('/test-runs/new', data={
            "run_code": "TR-REG-099",
            "name": "Regression Cycle for One-Click Checkout",
            "environment": "QA",
            "description": "Verify checkout regression stability."
        }, follow_redirects=True)
        assert run_resp.status_code == 200

        run_row = db.execute("SELECT id FROM test_runs WHERE run_code = 'TR-REG-099'").fetchone()
        assert run_row is not None
        run_id = run_row['id']

        # Record Failure in test execution
        exec_resp = client.post(f'/test-runs/{run_id}/execute/{tc_id}', data={
            "status": "Fail",
            "actual_result": "Button clicked but nothing happened; JavaScript uncaught error.",
            "executed_by": "Senior QA Engineer"
        }, follow_redirects=True)
        assert exec_resp.status_code == 200

        # Step 4: Raise Defect linked to Test Case & Run
        bug_resp = client.post('/defects/new', data={
            "bug_code": "BUG-REG-099",
            "title": "One-click button fails to trigger checkout event handler",
            "test_case_id": tc_id,
            "test_run_id": run_id,
            "severity": "Critical",
            "environment": "QA",
            "is_core_flow": "1",
            "steps_to_reproduce": "1. Navigate to product\n2. Click Instant Checkout\n3. Inspect console"
        }, follow_redirects=True)
        assert bug_resp.status_code == 200

        bug_row = db.execute("SELECT id FROM defects WHERE bug_code = 'BUG-REG-099'").fetchone()
        assert bug_row is not None
        bug_id = bug_row['id']

        # Step 5: Advance Defect through ISTQB Defect Lifecycle:
        # New -> Assigned -> Open -> Fixed -> Retest -> Closed
        client.post(f'/defects/{bug_id}/transition', data={"new_status": "Assigned", "notes": "Assigned to frontend lead"})
        client.post(f'/defects/{bug_id}/transition', data={"new_status": "Open", "notes": "Fix in progress"})
        client.post(f'/defects/{bug_id}/transition', data={"new_status": "Fixed", "notes": "Event listener attached properly in commit #abc12"})
        client.post(f'/defects/{bug_id}/transition', data={"new_status": "Retest", "notes": "Deployed to QA for verification"})
        client.post(f'/defects/{bug_id}/transition', data={"new_status": "Closed", "notes": "Retest passed successfully; defect closed"})

        final_bug = db.execute("SELECT status FROM defects WHERE id = ?", (bug_id,)).fetchone()
        assert final_bug['status'] == 'Closed'

        # Step 6: Verify Traceability Matrix (RTM) shows full linkage
        rtm = get_traceability_matrix(project_id=1)
        found_rtm = any(row['req_code'] == 'REQ-REG-99' and row['tc_code'] == 'TC-REG-099' for row in rtm['rows'])
        assert found_rtm is True

        # Step 7: Verify IEEE 829 Summary Report loads cleanly
        report_resp = client.get(f'/report/{run_id}')
        assert report_resp.status_code == 200
        assert "IEEE 829 Test Summary Report" in report_resp.get_data(as_text=True)
