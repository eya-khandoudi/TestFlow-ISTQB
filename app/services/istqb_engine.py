"""
ISTQB Domain Engine
Implements the core software testing concepts per ISTQB Foundation & Advanced Syllabus:
- State Transition Testing (Defect Lifecycle State Machine)
- Decision Table Testing (Defect SLA & Release Verdict Rules)
- Equivalence Partitioning & Boundary Value Analysis (Input Validators)
- Risk-Based Testing (Likelihood x Impact Matrix & Prioritization)
- Traceability (Forward and Backward Traceability analysis)
"""

class ISTQBValidationError(Exception):
    """Raised when an input violates EP or BVA rules."""
    pass

class InvalidStateTransitionError(Exception):
    """Raised when a state transition violates the ISTQB Defect Lifecycle."""
    pass

# ==============================================================================
# 1. STATE TRANSITION TESTING (Defect Lifecycle State Machine)
# ==============================================================================
# ISTQB Defect Lifecycle:
# New -> Assigned, Rejected, Deferred
# Assigned -> Open, Deferred, Rejected
# Open -> Fixed, Deferred, Rejected
# Fixed -> Retest
# Retest -> Closed (fix verified) OR Reopened (fix failed)
# Reopened -> Assigned, Open, Fixed
# Deferred -> Assigned, Open
# Rejected -> Closed, Reopened
# Closed -> Reopened

VALID_DEFECT_STATUSES = [
    'New', 'Assigned', 'Open', 'Fixed', 'Retest',
    'Closed', 'Reopened', 'Deferred', 'Rejected'
]

# Legal state transition graph: {from_status: [allowed_to_statuses]}
LEGAL_DEFECT_TRANSITIONS = {
    'New': ['Assigned', 'Rejected', 'Deferred'],
    'Assigned': ['Open', 'Deferred', 'Rejected'],
    'Open': ['Fixed', 'Deferred', 'Rejected'],
    'Fixed': ['Retest'],
    'Retest': ['Closed', 'Reopened'],
    'Reopened': ['Assigned', 'Open', 'Fixed'],
    'Deferred': ['Assigned', 'Open'],
    'Rejected': ['Closed', 'Reopened'],
    'Closed': ['Reopened']
}

def validate_defect_transition(current_status: str, new_status: str, notes: str = None) -> bool:
    """
    Validates a state transition in accordance with ISTQB State Transition rules.
    Raises InvalidStateTransitionError if transition is illegal.
    """
    if current_status not in VALID_DEFECT_STATUSES:
        raise InvalidStateTransitionError(f"Current status '{current_status}' is not a recognized ISTQB status.")
    
    if new_status not in VALID_DEFECT_STATUSES:
        raise InvalidStateTransitionError(f"Target status '{new_status}' is not a recognized ISTQB status.")

    if current_status == new_status:
        return True  # No state change, permissible update

    allowed_targets = LEGAL_DEFECT_TRANSITIONS.get(current_status, [])
    if new_status not in allowed_targets:
        allowed_str = ", ".join(f"'{s}'" for s in allowed_targets) if allowed_targets else "None (Terminal state)"
        raise InvalidStateTransitionError(
            f"Illegal state transition from '{current_status}' to '{new_status}'. "
            f"Allowed next states from '{current_status}' are: [{allowed_str}]."
        )

    # Business rule: Transitioning to Fixed, Rejected, or Deferred requires resolution notes
    if new_status in ['Fixed', 'Rejected', 'Deferred']:
        if not notes or not notes.strip():
            raise InvalidStateTransitionError(
                f"Transition to '{new_status}' requires resolution notes or justification."
            )

    return True

def get_allowed_transitions(current_status: str) -> list:
    """Returns a list of legal next statuses for the given status."""
    return LEGAL_DEFECT_TRANSITIONS.get(current_status, [])


# ==============================================================================
# 2. EQUIVALENCE PARTITIONING & BOUNDARY VALUE ANALYSIS (EP & BVA)
# ==============================================================================
def validate_risk_rating(rating: int, field_name: str = "Rating") -> int:
    """
    EP / BVA Validator for Risk Likelihood & Impact.
    Valid Partition: Integers in [1, 5]
    Boundaries: Min = 1, Max = 5
    Invalid Partitions: < 1 (e.g. 0, -1) and > 5 (e.g. 6, 100)
    """
    try:
        val = int(rating)
    except (ValueError, TypeError):
        raise ISTQBValidationError(f"{field_name} must be a valid integer between 1 and 5.")

    if val < 1:
        raise ISTQBValidationError(f"{field_name} boundary error: Value {val} is below minimum allowed (1).")
    if val > 5:
        raise ISTQBValidationError(f"{field_name} boundary error: Value {val} exceeds maximum allowed (5).")

    return val

def validate_string_length(text: str, min_len: int, max_len: int, field_name: str) -> str:
    """
    Validates text length with BVA.
    Boundaries tested: min_len - 1, min_len, max_len, max_len + 1.
    """
    if text is None:
        text = ""
    stripped = text.strip()
    length = len(stripped)
    if length < min_len:
        raise ISTQBValidationError(f"{field_name} must have at least {min_len} characters (got {length}).")
    if length > max_len:
        raise ISTQBValidationError(f"{field_name} must not exceed {max_len} characters (got {length}).")
    return stripped

def validate_cart_quantity(qty: int) -> int:
    """
    EP / BVA Validator for Cart Line Item Quantity (from project requirements).
    Valid Partition: [1, 99]
    Invalid Lower: <= 0
    Invalid Upper: >= 100
    """
    try:
        q = int(qty)
    except (ValueError, TypeError):
        raise ISTQBValidationError("Quantity must be a valid integer.")
    
    if q < 1:
        raise ISTQBValidationError(f"Invalid cart quantity: {q}. Quantity must be at least 1.")
    if q > 99:
        raise ISTQBValidationError(f"Invalid cart quantity: {q}. Quantity exceeds maximum allowable limit of 99.")
    return q


# ==============================================================================
# 3. RISK-BASED TESTING (RBT)
# ==============================================================================
def calculate_risk(likelihood: int, impact: int) -> dict:
    """
    Computes Risk Priority Number (RPN) = Likelihood (1-5) * Impact (1-5).
    Score range: 1 to 25.
    Categories:
    - 16 - 25: Critical (Red)
    - 10 - 15: High (Orange)
    - 5 - 9:   Medium (Yellow)
    - 1 - 4:   Low (Green)
    """
    l = validate_risk_rating(likelihood, "Likelihood")
    i = validate_risk_rating(impact, "Impact")
    score = l * i

    if score >= 16:
        category = "Critical"
        badge_class = "danger"
    elif score >= 10:
        category = "High"
        badge_class = "warning"
    elif score >= 5:
        category = "Medium"
        badge_class = "info"
    else:
        category = "Low"
        badge_class = "success"

    return {
        "likelihood": l,
        "impact": i,
        "score": score,
        "category": category,
        "badge_class": badge_class
    }


# ==============================================================================
# 4. DECISION TABLE TESTING (DTT)
# ==============================================================================
# Decision Table 1: Defect Triage & SLA Priority
# Conditions:
# C1: Severity in ['Blocker', 'Critical'] (True/False)
# C2: Environment == 'Production' (True/False)
# C3: Affects Core Payment / Auth Flow (True/False)
# Actions:
# Priority: Urgent, High, Medium, Low
# SLA Hours: 4, 12, 48, 120
# Escalation: True/False

def triage_defect_decision_table(severity: str, environment: str, is_core_flow: bool) -> dict:
    """
    Evaluates defect triage based on an ISTQB Decision Table.
    """
    sev = severity.strip().capitalize()
    env = environment.strip().upper()

    # Rule 1: Blocker/Critical in Production -> Immediate Urgent Escalation (4h SLA)
    if sev in ['Blocker', 'Critical'] and env == 'PRODUCTION':
        return {"priority": "Urgent", "sla_hours": 4, "escalation_required": True, "rule": "R1: Critical Prod Incident"}

    # Rule 2: Blocker/Critical in Staging/QA on Core Flow -> Urgent (8h SLA)
    if sev in ['Blocker', 'Critical'] and is_core_flow:
        return {"priority": "Urgent", "sla_hours": 8, "escalation_required": True, "rule": "R2: Core Flow Blocker"}

    # Rule 3: Blocker/Critical in QA on non-core -> High (16h SLA)
    if sev in ['Blocker', 'Critical'] and not is_core_flow:
        return {"priority": "High", "sla_hours": 16, "escalation_required": False, "rule": "R3: Non-core Critical QA Bug"}

    # Rule 4: Major Severity on Core Flow -> High (24h SLA)
    if sev == 'Major' and is_core_flow:
        return {"priority": "High", "sla_hours": 24, "escalation_required": False, "rule": "R4: Major Core Flow Issue"}

    # Rule 5: Major Severity on Non-Core Flow -> Medium (48h SLA)
    if sev == 'Major' and not is_core_flow:
        return {"priority": "Medium", "sla_hours": 48, "escalation_required": False, "rule": "R5: Major Secondary Issue"}

    # Rule 6: Minor Severity (Any Environment) -> Low (120h SLA)
    if sev == 'Minor':
        return {"priority": "Low", "sla_hours": 120, "escalation_required": False, "rule": "R6: Minor Cosmetic / Trivial"}

    # Default fallback rule
    return {"priority": "Medium", "sla_hours": 48, "escalation_required": False, "rule": "R7: Default Triage"}


# Decision Table 2: Release Gate Decision (Go / No-Go)
# Conditions:
# C1: Has any unresolved Blocker/Critical bugs (True/False)
# C2: Pass Rate >= 90% (True/False)
# C3: 100% of Critical Test Cases Passed (True/False)
# Actions:
# Decision: GO, NO-GO, CONDITIONAL-GO

def evaluate_release_gate(open_blockers: int, pass_rate: float, critical_tests_passed: bool) -> dict:
    """
    ISTQB Decision Table for Release Exit Criteria (IEEE 829 Test Summary Report).
    """
    if open_blockers > 0:
        return {
            "verdict": "NO-GO",
            "css_class": "danger",
            "reason": f"Gate blocked: Found {open_blockers} unresolved Blocker/Critical defects."
        }

    if pass_rate >= 90.0 and critical_tests_passed:
        return {
            "verdict": "GO",
            "css_class": "success",
            "reason": f"All release criteria met. Pass rate is {pass_rate:.1f}% with zero blocker bugs and 100% critical test pass."
        }

    if pass_rate >= 75.0 and critical_tests_passed:
        return {
            "verdict": "CONDITIONAL GO",
            "css_class": "warning",
            "reason": f"Pass rate ({pass_rate:.1f}%) meets threshold for beta/staging, but requires stakeholder sign-off."
        }

    return {
        "verdict": "NO-GO",
        "css_class": "danger",
        "reason": f"Pass rate ({pass_rate:.1f}%) is below minimum acceptance threshold (90%), or critical tests failed."
    }
