# pyright: basic
"""Unit tests for validators.between, written by Atifa Saqib.

Techniques: ECP (equivalence classes) and BVA (boundary values).
Reference range for most tests: min_val=1, max_val=100.
"""
import pytest

from validators import ValidationError, between

LOW = 1
HIGH = 100


# ---------- ECP: one test per equivalence class ----------

def test_value_inside_range():
    """ECP valid class: a value in the middle passes."""
    assert between(50, min_val=LOW, max_val=HIGH) is True


@pytest.mark.parametrize("value", [-5, 250])
def test_value_outside_range(value):
    """ECP invalid classes: below the range and above the range."""
    assert isinstance(between(value, min_val=LOW, max_val=HIGH), ValidationError)


def test_decimal_inside_range():
    """ECP: decimal numbers work, not only integers."""
    assert between(99.5, min_val=LOW, max_val=HIGH) is True


def test_negative_range():
    """ECP: ranges made of negative numbers work."""
    assert between(-5, min_val=-10, max_val=-1) is True


def test_only_min_given():
    """ECP: with no max_val, only the minimum is checked."""
    assert between(1000, min_val=LOW) is True


def test_only_max_given():
    """ECP: with no min_val, only the maximum is checked."""
    assert isinstance(between(5, max_val=0), ValidationError)


def test_no_limits():
    """With neither limit, any value is accepted."""
    assert between(42) is True


def test_none_is_rejected():
    """ECP invalid class: None fails validation."""
    assert isinstance(between(None, min_val=LOW, max_val=HIGH), ValidationError)


def test_text_inside_alphabetical_range():
    """ECP: text is compared alphabetically."""
    assert between("mango", min_val="apple", max_val="zebra") is True


# ---------- BVA: values at and around each boundary ----------

@pytest.mark.parametrize(
    ("value", "expected_ok"),
    [
        (0, False),    # just below min
        (1, True),     # min
        (2, True),     # just above min
        (99, True),    # just below max
        (100, True),   # max
        (101, False),  # just above max
    ],
)
def test_integer_boundaries(value, expected_ok):
    """BVA: both edges are valid, one step outside is not."""
    result = between(value, min_val=LOW, max_val=HIGH)
    assert (result is True) == expected_ok


@pytest.mark.parametrize(
    ("value", "expected_ok"),
    [(0.99, False), (1.0, True), (100.01, False)],
)
def test_decimal_boundaries(value, expected_ok):
    """BVA: the same edges, tested with decimal numbers."""
    result = between(value, min_val=LOW, max_val=HIGH)
    assert (result is True) == expected_ok


def test_min_equals_max():
    """BVA: when both limits are equal, only that value passes."""
    assert between(7, min_val=7, max_val=7) is True
    assert isinstance(between(8, min_val=7, max_val=7), ValidationError)


# ---------- Error cases ----------
# The docstring promises ValueError / TypeError, but the @validator wrapper
# returns a ValidationError instead. These tests record the real behaviour.

def test_reversed_limits():
    """min_val greater than max_val is an invalid configuration."""
    assert isinstance(between(50, min_val=100, max_val=1), ValidationError)


def test_type_mismatch():
    """Comparing text with numbers cannot succeed."""
    assert isinstance(between("abc", min_val=LOW, max_val=HIGH), ValidationError)