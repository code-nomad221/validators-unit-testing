"""Unit tests for validators.email, written by Amna Wahab.

Techniques used: ECP (valid and invalid format classes) and BVA (username
length limit of 64 characters). Results marked "predicted" were derived
from reading the source and are confirmed by running these tests.
"""
import pytest

from validators import ValidationError, email


# ---------- ECP: valid classes ----------

@pytest.mark.parametrize(
    "value",
    [
        "user@example.com",
        "first.last@example.com",
        "user+tag@example.com",
        "user@sub.example.com",
        "USER@EXAMPLE.COM",
    ],
)
def test_valid_emails_return_true(value):
    """ECP valid classes: plain, dotted, plus-tag, subdomain, uppercase."""
    assert email(value) is True


# ---------- ECP: invalid classes ----------

@pytest.mark.parametrize(
    "value",
    [
        "userexample.com",        # no @
        "user@@example.com",      # two @
        "user@",                  # missing domain
        "@example.com",           # missing username
        "user name@example.com",  # space in username
        ".user@example.com",      # dot at the start
        "user.@example.com",      # dot at the end
        "us..er@example.com",     # two dots in a row
        "user@example",           # no top-level domain
    ],
)
def test_invalid_formats_return_validation_error(value):
    """ECP invalid classes: each value breaks exactly one rule."""
    assert isinstance(email(value), ValidationError)


@pytest.mark.parametrize("value", ["", None])
def test_empty_or_missing_value_returns_validation_error(value):
    """ECP invalid class: empty string and None are rejected first."""
    assert isinstance(email(value), ValidationError)


# ---------- BVA: username length limit (maximum 64) ----------

@pytest.mark.parametrize(
    ("size", "should_pass"),
    [
        (1, True),    # shortest useful username
        (63, True),   # just below the limit
        (64, True),   # exactly the limit
        (65, False),  # just above the limit
    ],
)
def test_username_length_boundaries(size, should_pass):
    """BVA: usernames up to 64 characters pass, 65 fails."""
    result = email("a" * size + "@example.com")
    if should_pass:
        assert result is True
    else:
        assert isinstance(result, ValidationError)


# ---------- Optional flags ----------

def test_simple_host_flag():
    """A host without a dot is rejected unless simple_host=True."""
    assert isinstance(email("user@localhost"), ValidationError)
    assert email("user@localhost", simple_host=True) is True


def test_ipv4_domain_needs_brackets_and_flag():
    """predicted: IP domains must be in [brackets] and use ipv4_address."""
    assert email("user@[192.168.1.1]", ipv4_address=True) is True
    assert isinstance(email("user@192.168.1.1", ipv4_address=True), ValidationError)
    assert isinstance(email("user@[192.168.1.1]"), ValidationError)


def test_ipv6_domain_with_flag():
    """predicted: an IPv6 domain in brackets passes with ipv6_address."""
    assert email("user@[2001:db8::1]", ipv6_address=True) is True


def test_trailing_dot_needs_rfc_1034_flag():
    """predicted: a trailing dot in the domain needs rfc_1034=True."""
    assert isinstance(email("user@example.com."), ValidationError)
    assert email("user@example.com.", rfc_1034=True) is True