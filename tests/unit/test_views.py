"""
Unit and View integration tests for TestFlow web views.
Ensures full coverage of Flask routes, filters, and templates.
"""
import pytest

@pytest.mark.unit
class TestWebViews:

    def test_dashboard_view(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "QA Testing Dashboard" in html
        assert "IEEE 829 Release Gate Decision" in html

    def test_rtm_view(self, client):
        resp = client.get('/rtm')
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "Requirements Traceability Matrix" in html
        assert "REQ-AUTH-01" in html

    def test_istqb_guide_view(self, client):
        resp = client.get('/istqb-guide')
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "ISTQB Testing Methodologies in TestFlow" in html
        assert "Equivalence Partitioning" in html
        assert "Boundary Value Analysis" in html

    def test_test_summary_report_view(self, client):
        resp = client.get('/report/1')
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "IEEE 829 Test Summary Report" in html

    def test_requirements_crud_views(self, client, db):
        # List
        resp = client.get('/requirements/')
        assert resp.status_code == 200

        # Form GET
        resp_new = client.get('/requirements/new')
        assert resp_new.status_code == 200

        # Edit GET
        resp_edit = client.get('/requirements/1/edit')
        assert resp_edit.status_code == 200

        # Edit POST
        resp_edit_post = client.post('/requirements/1/edit', data={
            "title": "Updated Auth Title",
            "category": "Security",
            "priority": "Critical",
            "description": "Updated description"
        }, follow_redirects=True)
        assert resp_edit_post.status_code == 200

        # Delete
        resp_del = client.post('/requirements/1/delete', follow_redirects=True)
        assert resp_del.status_code == 200

    def test_test_cases_views(self, client):
        # List with filters
        resp = client.get('/test-cases/?sort=priority&type=Functional&priority=High')
        assert resp.status_code == 200

        # Detail view
        resp_detail = client.get('/test-cases/1')
        assert resp_detail.status_code == 200
        assert "TC-EP-001" in resp_detail.get_data(as_text=True)

        # Edit GET
        resp_edit = client.get('/test-cases/1/edit')
        assert resp_edit.status_code == 200

        # Edit POST
        resp_edit_post = client.post('/test-cases/1/edit', data={
            "title": "Updated Title for TC1",
            "steps": "1. New step\n2. New step",
            "expected_result": "Updated expected",
            "test_type": "Functional",
            "priority": "High",
            "risk_likelihood": 4,
            "risk_impact": 4
        }, follow_redirects=True)
        assert resp_edit_post.status_code == 200

        # Delete
        resp_del = client.post('/test-cases/1/delete', follow_redirects=True)
        assert resp_del.status_code == 200

    def test_test_runs_views(self, client):
        # List
        resp = client.get('/test-runs/')
        assert resp.status_code == 200

        # Detail
        resp_detail = client.get('/test-runs/1')
        assert resp_detail.status_code == 200

    def test_defects_views_and_filters(self, client):
        # List with filters
        resp = client.get('/defects/?status=Open&severity=Critical')
        assert resp.status_code == 200

        # Detail
        resp_detail = client.get('/defects/1')
        assert resp_detail.status_code == 200
        assert "BUG-001" in resp_detail.get_data(as_text=True)
