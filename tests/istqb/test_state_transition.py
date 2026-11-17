"""
ISTQB Test Technique: State Transition Testing (STT)
Specification-based testing technique where test cases are designed to execute
valid and invalid state transitions of the system state machine.
Covering 0-switch transitions, valid state paths, and illegal transition rejections.
"""
import pytest
from app.services.istqb_engine import (
    validate_defect_transition,
    get_allowed_transitions,
    InvalidStateTransitionError
)

@pytest.mark.state_transition
class TestStateTransitionTesting:

    # -------------------------------------------------------------------------
    # Positive STT: Happy Path (New -> Assigned -> Open -> Fixed -> Retest -> Closed)
    # -------------------------------------------------------------------------
    def test_happy_path_defect_lifecycle(self):
        # 1. New -> Assigned
        assert validate_defect_transition('New', 'Assigned') is True
        # 2. Assigned -> Open
        assert validate_defect_transition('Assigned', 'Open') is True
        # 3. Open -> Fixed (requires notes)
        assert validate_defect_transition('Open', 'Fixed', notes='Fixed in PR #104') is True
        # 4. Fixed -> Retest
        assert validate_defect_transition('Fixed', 'Retest') is True
        # 5. Retest -> Closed (fix verified)
        assert validate_defect_transition('Retest', 'Closed') is True

    # -------------------------------------------------------------------------
    # Positive STT: Reopen Path (Retest fails -> Reopened -> Fixed -> Retest -> Closed)
    # -------------------------------------------------------------------------
    def test_reopen_defect_lifecycle(self):
        # Retest failed -> Reopened
        assert validate_defect_transition('Retest', 'Reopened') is True
        # Reopened -> Open
        assert validate_defect_transition('Reopened', 'Open') is True
        # Open -> Fixed
        assert validate_defect_transition('Open', 'Fixed', notes='Second fix attempt') is True
        # Fixed -> Retest
        assert validate_defect_transition('Fixed', 'Retest') is True
        # Retest -> Closed
        assert validate_defect_transition('Retest', 'Closed') is True

    # -------------------------------------------------------------------------
    # Positive STT: Rejection & Deferred Paths
    # -------------------------------------------------------------------------
    def test_rejection_path(self):
        # New -> Rejected (requires justification)
        assert validate_defect_transition('New', 'Rejected', notes='Expected behavior per spec section 4') is True
        # Rejected -> Closed
        assert validate_defect_transition('Rejected', 'Closed') is True

    def test_deferred_path(self):
        # New -> Deferred
        assert validate_defect_transition('New', 'Deferred', notes='Postponed to Sprint 4') is True
        # Deferred -> Assigned
        assert validate_defect_transition('Deferred', 'Assigned') is True

    # -------------------------------------------------------------------------
    # Negative STT: Illegal State Transitions (Must be blocked by state engine)
    # -------------------------------------------------------------------------
    def test_illegal_transition_new_to_closed(self):
        """ISTQB rule: Defect cannot jump directly from New to Closed without resolution or rejection."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            validate_defect_transition('New', 'Closed')
        assert "Illegal state transition" in str(exc_info.value)

    def test_illegal_transition_open_to_closed(self):
        """ISTQB rule: Defect cannot be Closed directly while still Open without Fixed & Retest."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            validate_defect_transition('Open', 'Closed')
        assert "Illegal state transition" in str(exc_info.value)

    def test_illegal_transition_fixed_to_closed(self):
        """ISTQB rule: Developer cannot close Fixed defect directly; QA must Retest it first!"""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            validate_defect_transition('Fixed', 'Closed')
        assert "Illegal state transition" in str(exc_info.value)

    def test_illegal_transition_new_to_retest(self):
        """Defect cannot be Retested if it was never Fixed."""
        with pytest.raises(InvalidStateTransitionError):
            validate_defect_transition('New', 'Retest')

    def test_fixed_without_resolution_notes_rejected(self):
        """Business rule: Marking Fixed requires developer resolution notes."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            validate_defect_transition('Open', 'Fixed', notes="")
        assert "requires resolution notes" in str(exc_info.value)

    def test_allowed_transitions_query(self):
        """Verify helper returns correct next states for UI buttons."""
        allowed = get_allowed_transitions('New')
        assert 'Assigned' in allowed
        assert 'Rejected' in allowed
        assert 'Deferred' in allowed
        assert 'Closed' not in allowed
