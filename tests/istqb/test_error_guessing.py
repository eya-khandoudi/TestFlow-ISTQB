"""
ISTQB Test Technique: Error Guessing
Experience-based testing technique where the tester anticipates errors, defects,
and vulnerabilities based on knowledge, past experience, and common failure modes.
"""
import pytest
from app.services.istqb_engine import validate_string_length, ISTQBValidationError

@pytest.mark.error_guessing
class TestErrorGuessing:

    def test_sql_injection_payload_handled_safely(self, client):
        """Error Guessing: Test resilience against classic SQL injection attempts."""
        sqli_payload = "'; DROP TABLE test_cases; --"
        response = client.post('/api/test-cases', json={
            "tc_code": "TC-SQL-01",
            "title": sqli_payload,
            "steps": "1. Test step with " + sqli_payload,
            "expected_result": "Input sanitized safely",
            "risk_likelihood": 2,
            "risk_impact": 4
        })
        # Should create record with parameterized query without breaking database
        assert response.status_code == 201

        # Verify table still exists and query executes cleanly
        metrics_resp = client.get('/api/metrics')
        assert metrics_resp.status_code == 200

    def test_xss_payload_in_defect_title(self, client):
        """Error Guessing: Attempt Cross-Site Scripting payload injection."""
        xss_payload = "<script>alert('XSS-Exploit')</script>"
        response = client.post('/api/defects', json={
            "bug_code": "BUG-XSS-1",
            "title": xss_payload,
            "steps_to_reproduce": "Step 1: Injected " + xss_payload,
            "severity": "Critical",
            "environment": "QA"
        })
        assert response.status_code == 201

        # Check that UI renders with proper HTML escaping
        html_resp = client.get('/defects/')
        assert html_resp.status_code == 200
        # Should not execute raw script tag in unescaped manner
        assert "<script>alert('XSS-Exploit')</script>" not in html_resp.get_data(as_text=True) or \
               "&lt;script&gt;" in html_resp.get_data(as_text=True)

    def test_unicode_and_emojis_in_test_steps(self, client):
        """Error Guessing: Non-ASCII characters, emojis, and right-to-left scripts."""
        unicode_title = "Verify Arabic: تجربة فحص and Emoji 🚀🔥💯"
        response = client.post('/api/test-cases', json={
            "tc_code": "TC-UNI-01",
            "title": unicode_title,
            "steps": "خطوات الاختبار مع الرموز 🎯",
            "expected_result": "Handled without UTF-8 decode error",
            "risk_likelihood": 1,
            "risk_impact": 1
        })
        assert response.status_code == 201

    def test_whitespace_only_string_rejected(self):
        """Error Guessing: Input consisting exclusively of whitespace/spaces."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_string_length("     ", 5, 200, "Title")
        assert "at least 5 characters" in str(exc_info.value)

    def test_invalid_foreign_key_handled(self, client):
        """Error Guessing: Submitting non-existent requirement_id."""
        response = client.post('/api/test-cases', json={
            "tc_code": "TC-FK-99",
            "title": "Invalid Foreign Key Case",
            "steps": "Step 1",
            "expected_result": "Result",
            "requirement_id": 999999  # Does not exist
        })
        # Database foreign key constraint fails safely
        assert response.status_code == 400
