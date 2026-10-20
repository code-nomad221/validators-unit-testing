# pyright: basic
"""Unit tests for validators.length, written by Atifa Saqib.

Techniques: ECP (equivalence classes) and BVA (boundary values).
Reference range for most tests: min_val=5, max_val=12 (string length).
"""
import pytest

from validators import ValidationError, length

pytestmark = pytest.mark.group_length

LOW = 5
HIGH = 12


# ---------- ECP: one test per equivalence class ----------

@pytest.mark.ecp
@pytest.mark.smoke
@pytest.mark.case_order(1)
@pytest.mark.parametrize("text", ["hello", "keyboard"])
def test_length_inside_range(text):
    """ECP valid class: lengths 5 and 8 are inside 5 to 12."""
    assert length(text, min_val=LOW, max_val=HIGH) is True


@pytest.mark.ecp
@pytest.mark.negative
@pytest.mark.parametrize("text", ["hi", "a" * 20])
def test_length_outside_range(text):
    """ECP invalid classes: too short and too long."""
    assert isinstance(length(text, min_val=LOW, max_val=HIGH), ValidationError)


@pytest.mark.ecp
def test_only_min_given():
    """ECP: with no max_val, only the minimum is checked."""
    assert length("python", min_val=3) is True


@pytest.mark.ecp
def test_only_max_given():
    """ECP: with no min_val, only the maximum is checked."""
    assert isinstance(length("python", max_val=3), ValidationError)


@pytest.mark.ecp
def test_no_limits():
    """With no limits, any string passes."""
    assert length("anything") is True


@pytest.mark.ecp
def test_empty_string_no_limits():
    """ECP: the empty string has length 0 and nothing rejects it."""
    assert length("") is True


@pytest.mark.ecp
@pytest.mark.negative
def test_empty_string_with_min_one():
    """ECP: the empty string is too short when min_val is 1."""
    assert isinstance(length("", min_val=1), ValidationError)


@pytest.mark.ecp
def test_spaces_count_as_characters():
    """ECP: five spaces are five characters."""
    assert length("     ", min_val=LOW, max_val=HIGH) is True


@pytest.mark.ecp
def test_non_english_letters():
    """ECP: accented letters count as one character each."""
    assert length("héllo wörld", min_val=LOW, max_val=HIGH) is True


# ---------- BVA: lengths at and around each boundary ----------

@pytest.mark.bva
@pytest.mark.parametrize(
    ("size", "expected_ok"),
    [
        (4, False),   # just below min
        (5, True),    # min
        (6, True),    # just above min
        (11, True),   # just below max
        (12, True),   # max
        (13, False),  # just above max
    ],
)
def test_length_boundaries(size, expected_ok):
    """BVA: both edges are valid, one step outside is not."""
    result = length("x" * size, min_val=LOW, max_val=HIGH)
    assert (result is True) == expected_ok


@pytest.mark.bva
def test_zero_is_lowest_allowed_limit():
    """BVA: min_val=0 is allowed, so the empty string passes."""
    assert length("", min_val=0) is True


@pytest.mark.bva
def test_min_equals_max():
    """BVA: when both limits are equal, only that exact length passes."""
    assert length("sixsix", min_val=6, max_val=6) is True
    assert isinstance(length("seven77", min_val=6, max_val=6), ValidationError)


# ---------- Error cases ----------
# The code raises ValueError for negative limits, but the @validator wrapper
# returns a ValidationError instead. These tests record the real behaviour.

@pytest.mark.negative
@pytest.mark.parametrize(
    ("min_val", "max_val"),
    [(-1, None), (None, -1), (10, 2)],
)
def test_invalid_limits(min_val, max_val):
    """Negative limits and reversed limits are invalid configurations."""
    assert isinstance(length("abc", min_val=min_val, max_val=max_val), ValidationError)


@pytest.mark.negative
def test_number_instead_of_text():
    """A number has no length, so the check cannot succeed."""
    assert isinstance(length(12345, min_val=1, max_val=10), ValidationError)  # type: ignore[arg-type]
