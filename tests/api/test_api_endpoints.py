"""
REST API Integration Tests for TestFlow
Tests all backend API endpoints used for CI/CD integration and test automation.
"""
import pytest

@pytest.mark.api
class TestApiEndpoints:

    def test_health_check(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'healthy'
        assert "TestFlow" in data['service']

    def test_get_metrics(self, client):
        resp = client.get('/api/metrics')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'pass_rate' in data
        assert 'total_executions' in data
        assert 'release_gate' in data
        assert data['tc_count'] > 0

    def test_get_requirements(self, client):
        resp = client.get('/api/requirements')
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) >= 5

    def test_create_test_case_api(self, client):
        payload = {
            "tc_code": "TC-API-001",
            "title": "API Automated Checkout Verification",
            "steps": "1. Send POST /api/checkout\n2. Verify 200 OK",
            "expected_result": "Order ID returned in JSON payload",
            "test_type": "Functional",
            "priority": "High",
            "risk_likelihood": 3,
            "risk_impact": 4
        }
        resp = client.post('/api/test-cases', json=payload)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['tc_code'] == 'TC-API-001'
        assert data['status'] == 'created'

    def test_record_test_execution_api(self, client):
        payload = {
            "test_case_id": 1,
            "status": "Pass",
            "actual_result": "Passed via Automated CI Runner",
            "executed_by": "Pytest Automation Bot"
        }
        resp = client.post('/api/test-runs/1/executions', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'Pass'

    def test_defect_lifecycle_transition_via_api(self, client):
        # 1. Create a new defect
        payload = {
            "bug_code": "BUG-API-01",
            "title": "API Discovered Defect in Checkout",
            "steps_to_reproduce": "1. Post malformed JSON\n2. Server 500",
            "severity": "Major",
            "environment": "QA"
        }
        create_resp = client.post('/api/defects', json=payload)
        assert create_resp.status_code == 201
        bug_id = create_resp.get_json()['id']

        # 2. Transition New -> Assigned (Legal)
        trans1 = client.post(f'/api/defects/{bug_id}/transition', json={
            "new_status": "Assigned",
            "notes": "Assigned to backend lead"
        })
        assert trans1.status_code == 200
        assert trans1.get_json()['new_status'] == 'Assigned'

        # 3. Attempt Illegal transition Assigned -> Closed (Must return 422 Unprocessable)
        trans2 = client.post(f'/api/defects/{bug_id}/transition', json={
            "new_status": "Closed",
            "notes": "Skipping fix and retest"
        })
        assert trans2.status_code == 422
        assert trans2.get_json()['error'] == 'InvalidStateTransitionError'

    def test_istqb_triage_decision_table_api(self, client):
        resp = client.post('/api/istqb/triage', json={
            "severity": "Blocker",
            "environment": "Production",
            "is_core_flow": True
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['priority'] == 'Urgent'
        assert data['sla_hours'] == 4

    def test_istqb_cart_bva_api(self, client):
        # Boundary: 99 (valid)
        resp_valid = client.post('/api/istqb/validate-cart', json={"quantity": 99})
        assert resp_valid.status_code == 200
        assert resp_valid.get_json()['status'] == 'valid'

        # Boundary: 100 (invalid)
        resp_invalid = client.post('/api/istqb/validate-cart', json={"quantity": 100})
        assert resp_invalid.status_code == 400
        assert resp_invalid.get_json()['status'] == 'invalid'
