"""
ISTQB Test Technique: Boundary Value Analysis (BVA)
Specification-based testing technique based on testing at the boundaries of equivalence partitions.
Tests both 2-value BVA (boundary, boundary + 1 / boundary - 1) and 3-value BVA.
"""
import pytest
from app.services.istqb_engine import (
    validate_cart_quantity,
    validate_risk_rating,
    validate_string_length,
    ISTQBValidationError
)

@pytest.mark.boundary_value_analysis
class TestBoundaryValueAnalysis:

    # -------------------------------------------------------------------------
    # BVA 1: Cart Quantity [1, 99]
    # Boundaries:
    # 0  : Just below minimum (Invalid)
    # 1  : Minimum valid boundary (Valid)
    # 2  : Just above minimum (Valid)
    # 98 : Just below maximum (Valid)
    # 99 : Maximum valid boundary (Valid)
    # 100: Just above maximum (Invalid)
    # -------------------------------------------------------------------------
    def test_cart_quantity_below_min_boundary(self):
        """Boundary: 0 (Min - 1) -> Invalid"""
        with pytest.raises(ISTQBValidationError):
            validate_cart_quantity(0)

    def test_cart_quantity_min_boundary(self):
        """Boundary: 1 (Min) -> Valid"""
        assert validate_cart_quantity(1) == 1

    def test_cart_quantity_just_above_min_boundary(self):
        """Boundary: 2 (Min + 1) -> Valid"""
        assert validate_cart_quantity(2) == 2

    def test_cart_quantity_just_below_max_boundary(self):
        """Boundary: 98 (Max - 1) -> Valid"""
        assert validate_cart_quantity(98) == 98

    def test_cart_quantity_max_boundary(self):
        """Boundary: 99 (Max) -> Valid"""
        assert validate_cart_quantity(99) == 99

    def test_cart_quantity_above_max_boundary(self):
        """Boundary: 100 (Max + 1) -> Invalid"""
        with pytest.raises(ISTQBValidationError):
            validate_cart_quantity(100)

    # -------------------------------------------------------------------------
    # BVA 2: Risk Rating [1, 5]
    # Boundaries: 0, 1, 2, 4, 5, 6
    # -------------------------------------------------------------------------
    def test_risk_rating_below_min_boundary(self):
        """Boundary: 0 -> Invalid"""
        with pytest.raises(ISTQBValidationError):
            validate_risk_rating(0)

    def test_risk_rating_min_boundary(self):
        """Boundary: 1 -> Valid"""
        assert validate_risk_rating(1) == 1

    def test_risk_rating_just_above_min_boundary(self):
        """Boundary: 2 -> Valid"""
        assert validate_risk_rating(2) == 2

    def test_risk_rating_just_below_max_boundary(self):
        """Boundary: 4 -> Valid"""
        assert validate_risk_rating(4) == 4

    def test_risk_rating_max_boundary(self):
        """Boundary: 5 -> Valid"""
        assert validate_risk_rating(5) == 5

    def test_risk_rating_above_max_boundary(self):
        """Boundary: 6 -> Invalid"""
        with pytest.raises(ISTQBValidationError):
            validate_risk_rating(6)

    # -------------------------------------------------------------------------
    # BVA 3: Identifier Code Length [3, 20]
    # Boundaries: 2, 3, 20, 21
    # -------------------------------------------------------------------------
    def test_code_length_just_below_min(self):
        """Length: 2 -> Invalid"""
        with pytest.raises(ISTQBValidationError):
            validate_string_length("TC", 3, 20, "Code")

    def test_code_length_min_boundary(self):
        """Length: 3 -> Valid"""
        assert validate_string_length("TC1", 3, 20, "Code") == "TC1"

    def test_code_length_max_boundary(self):
        """Length: 20 -> Valid"""
        code_20 = "TC-VERY-LONG-CODE-20"
        assert len(code_20) == 20
        assert validate_string_length(code_20, 3, 20, "Code") == code_20

    def test_code_length_just_above_max(self):
        """Length: 21 -> Invalid"""
        code_21 = "TC-VERY-LONG-CODE-021"
        assert len(code_21) == 21
        with pytest.raises(ISTQBValidationError):
            validate_string_length(code_21, 3, 20, "Code")
