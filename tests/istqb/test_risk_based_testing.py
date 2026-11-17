"""
ISTQB Test Technique: Risk-Based Testing (RBT)
Testing technique in which test activities and prioritization are guided by product risk.
Validates the Risk Priority Number (RPN) = Likelihood * Impact formula and risk-based sorting.
"""
import pytest
from app.services.istqb_engine import calculate_risk
from app.services.report_service import get_dashboard_metrics

@pytest.mark.risk_based
class TestRiskBasedTesting:

    def test_critical_risk_classification(self):
        """RPN >= 16 must be classified as Critical (Red)."""
        # 4 * 4 = 16 (Boundary of Critical)
        r1 = calculate_risk(4, 4)
        assert r1['score'] == 16
        assert r1['category'] == 'Critical'
        assert r1['badge_class'] == 'danger'

        # 5 * 5 = 25 (Maximum possible RPN)
        r2 = calculate_risk(5, 5)
        assert r2['score'] == 25
        assert r2['category'] == 'Critical'

    def test_high_risk_classification(self):
        """10 <= RPN <= 15 must be classified as High (Orange/Warning)."""
        # 2 * 5 = 10 (Lower boundary of High)
        r1 = calculate_risk(2, 5)
        assert r1['score'] == 10
        assert r1['category'] == 'High'

        # 3 * 5 = 15 (Upper boundary of High)
        r2 = calculate_risk(3, 5)
        assert r2['score'] == 15
        assert r2['category'] == 'High'

    def test_medium_risk_classification(self):
        """5 <= RPN <= 9 must be classified as Medium (Yellow/Info)."""
        # 1 * 5 = 5 (Lower boundary)
        r1 = calculate_risk(1, 5)
        assert r1['score'] == 5
        assert r1['category'] == 'Medium'

        # 3 * 3 = 9 (Upper boundary)
        r2 = calculate_risk(3, 3)
        assert r2['score'] == 9
        assert r2['category'] == 'Medium'

    def test_low_risk_classification(self):
        """1 <= RPN <= 4 must be classified as Low (Green/Success)."""
        # 1 * 1 = 1 (Minimum possible RPN)
        r1 = calculate_risk(1, 1)
        assert r1['score'] == 1
        assert r1['category'] == 'Low'

        # 2 * 2 = 4 (Upper boundary of Low)
        r2 = calculate_risk(2, 2)
        assert r2['score'] == 4
        assert r2['category'] == 'Low'

    def test_test_run_prioritizes_highest_risk_first(self, client):
        """
        Verify that test run execution view sorts test scenarios by Risk Score descending.
        This guarantees that critical, high-risk scenarios are executed first.
        """
        response = client.get('/test-runs/1')
        assert response.status_code == 200

        # Run 1 has TC-PAY-010 (score 20) which should appear before low-risk tests
        html = response.get_data(as_text=True)
        idx_pay10 = html.find('TC-PAY-010')
        idx_ep001 = html.find('TC-EP-001')
        assert idx_pay10 != -1 and idx_ep001 != -1
        assert idx_pay10 < idx_ep001, "High-risk TC-PAY-010 should be prioritized before lower-risk tests"
