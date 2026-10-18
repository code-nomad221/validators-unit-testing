"""Unit tests for validators.between, written by Amna Wahab.

Techniques used: ECP (equivalence classes) and BVA (boundary values).
Reference range for most tests: min_val=10, max_val=20.
"""
from datetime import datetime

import pytest

from validators import ValidationError, between


# ---------- ECP: one test per equivalence class ----------

def test_value_inside_range_returns_true():
    """ECP valid class: a value inside the range passes."""
    assert between(15, min_val=10, max_val=20) is True


@pytest.mark.parametrize("value", [3, 50])
def test_value_outside_range_returns_validation_error(value):
    """ECP invalid classes: below the range (3) and above the range (50)."""
    assert isinstance(between(value, min_val=10, max_val=20), ValidationError)


def test_only_min_given():
    """ECP: only a minimum is checked when max_val is missing."""
    assert between(5, min_val=2) is True


def test_only_max_given():
    """ECP: only a maximum is checked when min_val is missing."""
    assert isinstance(between(500, max_val=400), ValidationError)


def test_no_limits_always_true():
    """Note in the source: with no limits the result is always True."""
    assert between(7) is True


def test_none_value_returns_validation_error():
    """ECP invalid class: None as the value fails validation."""
    assert isinstance(between(None, min_val=10, max_val=20), ValidationError)


@pytest.mark.parametrize(
    ("value", "min_val", "max_val"),
    [
        (13.2, 13, 14),
        (datetime(2000, 11, 11), datetime(1999, 11, 11), datetime(2001, 1, 1)),
        ("b", "a", "c"),
    ],
)
def test_other_value_types_inside_range(value, min_val, max_val):
    """ECP: floats, dates and text work, not only integers."""
    assert between(value, min_val=min_val, max_val=max_val) is True


# ---------- BVA: values at and around each boundary ----------

@pytest.mark.parametrize(
    ("value", "should_pass"),
    [
        (9, False),   # just below min
        (10, True),   # exactly min
        (11, True),   # just above min
        (19, True),   # just below max
        (20, True),   # exactly max
        (21, False),  # just above max
    ],
)
def test_boundary_values(value, should_pass):
    """BVA: both edges are inclusive, one step outside fails."""
    result = between(value, min_val=10, max_val=20)
    if should_pass:
        assert result is True
    else:
        assert isinstance(result, ValidationError)


def test_min_equals_max():
    """BVA: when both limits are the same, only that value is valid."""
    assert between(10, min_val=10, max_val=10) is True


def test_min_greater_than_max_returns_validation_error():
    """Docstring says ValueError, but the @validator wrapper returns
    a ValidationError instead. This test records the actual behaviour."""
    assert isinstance(between(15, min_val=20, max_val=10), ValidationError)

def test_type_mismatch_returns_validation_error():
    """Docstring says TypeError, but the @validator wrapper returns
    a ValidationError instead. This test records the actual behaviour."""
    assert isinstance(between("abc", min_val=10, max_val=20), ValidationError)   