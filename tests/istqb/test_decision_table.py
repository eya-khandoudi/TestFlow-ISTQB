"""
ISTQB Test Technique: Decision Table Testing (DTT)
Specification-based testing technique used to test combinations of conditions (inputs)
that produce actions (outputs).
"""
import pytest
from app.services.istqb_engine import triage_defect_decision_table, evaluate_release_gate

@pytest.mark.decision_table
class TestDecisionTableTesting:

    # -------------------------------------------------------------------------
    # Decision Table 1: Defect Triage & SLA Priority
    # Conditions:
    # C1: Severity in ['Blocker', 'Critical']
    # C2: Environment == 'Production'
    # C3: Affects Core Flow
    # Expected Actions:
    # Rule 1: [T, T, *] -> Priority: Urgent, SLA: 4h, Escalation: True
    # Rule 2: [T, F, T] -> Priority: Urgent, SLA: 8h, Escalation: True
    # Rule 3: [T, F, F] -> Priority: High,   SLA: 16h, Escalation: False
    # Rule 4: [Major, *, T] -> Priority: High, SLA: 24h
    # Rule 5: [Major, *, F] -> Priority: Medium, SLA: 48h
    # Rule 6: [Minor, *, *] -> Priority: Low, SLA: 120h
    # -------------------------------------------------------------------------
    def test_dt_rule_1_critical_production(self):
        result = triage_defect_decision_table('Blocker', 'Production', is_core_flow=False)
        assert result['priority'] == 'Urgent'
        assert result['sla_hours'] == 4
        assert result['escalation_required'] is True
        assert "R1" in result['rule']

    def test_dt_rule_2_critical_qa_core_flow(self):
        result = triage_defect_decision_table('Critical', 'QA', is_core_flow=True)
        assert result['priority'] == 'Urgent'
        assert result['sla_hours'] == 8
        assert result['escalation_required'] is True
        assert "R2" in result['rule']

    def test_dt_rule_3_critical_qa_non_core(self):
        result = triage_defect_decision_table('Critical', 'QA', is_core_flow=False)
        assert result['priority'] == 'High'
        assert result['sla_hours'] == 16
        assert result['escalation_required'] is False
        assert "R3" in result['rule']

    def test_dt_rule_4_major_core_flow(self):
        result = triage_defect_decision_table('Major', 'QA', is_core_flow=True)
        assert result['priority'] == 'High'
        assert result['sla_hours'] == 24
        assert result['escalation_required'] is False
        assert "R4" in result['rule']

    def test_dt_rule_5_major_secondary_flow(self):
        result = triage_defect_decision_table('Major', 'QA', is_core_flow=False)
        assert result['priority'] == 'Medium'
        assert result['sla_hours'] == 48
        assert result['escalation_required'] is False
        assert "R5" in result['rule']

    def test_dt_rule_6_minor_any_condition(self):
        result = triage_defect_decision_table('Minor', 'Production', is_core_flow=True)
        assert result['priority'] == 'Low'
        assert result['sla_hours'] == 120
        assert result['escalation_required'] is False
        assert "R6" in result['rule']

    # -------------------------------------------------------------------------
    # Decision Table 2: IEEE 829 Release Gate Decision
    # Conditions:
    # C1: Open Blockers > 0
    # C2: Pass Rate >= 90.0%
    # C3: 100% Critical Tests Passed
    # -------------------------------------------------------------------------
    def test_release_gate_no_go_due_to_blockers(self):
        """Open blockers > 0 -> NO-GO regardless of pass rate."""
        gate = evaluate_release_gate(open_blockers=1, pass_rate=98.0, critical_tests_passed=True)
        assert gate['verdict'] == 'NO-GO'
        assert "unresolved Blocker/Critical" in gate['reason']

    def test_release_gate_go_full_criteria_met(self):
        """Zero blockers + Pass Rate >= 90% + Critical passed -> GO."""
        gate = evaluate_release_gate(open_blockers=0, pass_rate=92.5, critical_tests_passed=True)
        assert gate['verdict'] == 'GO'
        assert "All release criteria met" in gate['reason']

    def test_release_gate_conditional_go(self):
        """Zero blockers + 75% <= Pass Rate < 90% + Critical passed -> CONDITIONAL GO."""
        gate = evaluate_release_gate(open_blockers=0, pass_rate=80.0, critical_tests_passed=True)
        assert gate['verdict'] == 'CONDITIONAL GO'

    def test_release_gate_no_go_failed_critical_tests(self):
        """Zero blockers but critical tests failed -> NO-GO."""
        gate = evaluate_release_gate(open_blockers=0, pass_rate=95.0, critical_tests_passed=False)
        assert gate['verdict'] == 'NO-GO'
