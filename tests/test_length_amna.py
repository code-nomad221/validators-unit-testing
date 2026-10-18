# pyright: basic
"""Unit tests for validators.length, written by Amna Wahab.

Techniques used: ECP (equivalence classes) and BVA (boundary values).
Reference range for most tests: min_val=3, max_val=8 (string length).
"""
import pytest

from validators import ValidationError, length


# ---------- ECP: one test per equivalence class ----------

def test_length_inside_range_returns_true():
    """ECP valid class: a length inside the range passes."""
    assert length("abcde", min_val=3, max_val=8) is True


@pytest.mark.parametrize("value", ["ab", "abcdefghijkl"])
def test_length_outside_range_returns_validation_error(value):
    """ECP invalid classes: too short and too long."""
    assert isinstance(length(value, min_val=3, max_val=8), ValidationError)


def test_only_min_given():
    """ECP: only the minimum is checked when max_val is missing."""
    assert length("something", min_val=2) is True


def test_only_max_given():
    """ECP: only the maximum is checked when min_val is missing."""
    assert isinstance(length("something", max_val=5), ValidationError)


def test_no_limits_always_true():
    """ECP: with no limits any string passes."""
    assert length("abc") is True


def test_empty_string_without_limits_is_valid():
    """ECP: the empty string has length 0, and no limit rejects it."""
    assert length("") is True


def test_empty_string_with_min_one_is_invalid():
    """ECP: the empty string is too short when min_val is 1."""
    assert isinstance(length("", min_val=1), ValidationError)


# ---------- BVA: lengths at and around each boundary ----------

@pytest.mark.parametrize(
    ("size", "should_pass"),
    [
        (2, False),  # just below min
        (3, True),   # exactly min
        (4, True),   # just above min
        (7, True),   # just below max
        (8, True),   # exactly max
        (9, False),  # just above max
    ],
)
def test_boundary_lengths(size, should_pass):
    """BVA: both edges are inclusive, one step outside fails."""
    result = length("a" * size, min_val=3, max_val=8)
    if should_pass:
        assert result is True
    else:
        assert isinstance(result, ValidationError)


def test_min_equals_max():
    """BVA: when both limits are equal, only that exact length is valid."""
    assert length("something", min_val=9, max_val=9) is True
    assert isinstance(length("somethin", min_val=9, max_val=9), ValidationError)


def test_zero_is_the_lowest_allowed_limit():
    """BVA: min_val=0 is allowed, so the empty string passes."""
    assert length("", min_val=0) is True


# ---------- Error cases (predicted: wrapper returns ValidationError) ----------

@pytest.mark.parametrize(
    ("min_val", "max_val"),
    [(-1, None), (None, -1), (8, 3)],
)
def test_invalid_limits_return_validation_error(min_val, max_val):
    """Negative limits and reversed limits are invalid configurations."""
    result = length("abc", min_val=min_val, max_val=max_val)
    assert isinstance(result, ValidationError)


def test_non_string_value_returns_validation_error():
    """A number has no length, so the check cannot succeed."""
    assert isinstance(length(12345, min_val=1, max_val=10), ValidationError)  # type: ignore[arg-type]