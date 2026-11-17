"""
ISTQB Test Technique: Equivalence Partitioning (EP)
Specification-based testing technique where input data is partitioned into equivalent classes
from which test cases are derived. Testing one value from each partition is assumed to be
representative of the entire class.
"""
import pytest
from app.services.istqb_engine import (
    validate_risk_rating,
    validate_string_length,
    validate_cart_quantity,
    ISTQBValidationError
)

@pytest.mark.equivalence_partitioning
class TestEquivalencePartitioning:

    # -------------------------------------------------------------------------
    # EP 1: Risk Likelihood / Impact Valid & Invalid Partitions
    # Valid Partition: Integers in [1, 5]
    # Invalid Partition A: Integers < 1
    # Invalid Partition B: Integers > 5
    # Invalid Partition C: Non-numeric values
    # -------------------------------------------------------------------------
    @pytest.mark.parametrize("valid_value", [1, 2, 3, 4, 5])
    def test_risk_rating_valid_partition(self, valid_value):
        """Partition 1: Any value within [1, 5] must pass validation."""
        result = validate_risk_rating(valid_value, "Likelihood")
        assert result == valid_value

    @pytest.mark.parametrize("invalid_low", [0, -1, -99])
    def test_risk_rating_invalid_low_partition(self, invalid_low):
        """Partition 2: Any value < 1 must be rejected."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_risk_rating(invalid_low, "Likelihood")
        assert "below minimum allowed" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_high", [6, 10, 50, 999])
    def test_risk_rating_invalid_high_partition(self, invalid_high):
        """Partition 3: Any value > 5 must be rejected."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_risk_rating(invalid_high, "Impact")
        assert "exceeds maximum allowed" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_type", ["abc", None, "", "invalid"])
    def test_risk_rating_invalid_type_partition(self, invalid_type):
        """Partition 4: Non-integer representations must be rejected."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_risk_rating(invalid_type, "Likelihood")
        assert "must be a valid integer" in str(exc_info.value)

    # -------------------------------------------------------------------------
    # EP 2: Cart Line Quantity Partitions
    # Valid Partition: Integers in [1, 99]
    # Invalid Lower Partition: Integers <= 0
    # Invalid Upper Partition: Integers >= 100
    # -------------------------------------------------------------------------
    @pytest.mark.parametrize("valid_qty", [1, 10, 50, 99])
    def test_cart_quantity_valid_partition(self, valid_qty):
        """Partition 1: Standard quantities between 1 and 99."""
        assert validate_cart_quantity(valid_qty) == valid_qty

    @pytest.mark.parametrize("invalid_low_qty", [0, -1, -50])
    def test_cart_quantity_invalid_low_partition(self, invalid_low_qty):
        """Partition 2: Zero or negative quantities."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_cart_quantity(invalid_low_qty)
        assert "must be at least 1" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_high_qty", [100, 150, 999])
    def test_cart_quantity_invalid_high_partition(self, invalid_high_qty):
        """Partition 3: Quantities exceeding allowed maximum."""
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_cart_quantity(invalid_high_qty)
        assert "exceeds maximum allowable limit" in str(exc_info.value)

    # -------------------------------------------------------------------------
    # EP 3: Text Field Length Partitions
    # Valid Partition: String length in [5, 200]
    # Invalid Underflow: String length < 5
    # Invalid Overflow: String length > 200
    # -------------------------------------------------------------------------
    def test_text_length_valid_partition(self):
        valid_text = "Valid Test Title Here"
        assert validate_string_length(valid_text, 5, 200, "Title") == valid_text

    def test_text_length_underflow_partition(self):
        short_text = "A"
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_string_length(short_text, 5, 200, "Title")
        assert "at least 5 characters" in str(exc_info.value)

    def test_text_length_overflow_partition(self):
        long_text = "X" * 201
        with pytest.raises(ISTQBValidationError) as exc_info:
            validate_string_length(long_text, 5, 200, "Title")
        assert "must not exceed 200 characters" in str(exc_info.value)
