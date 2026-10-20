# pyright: basic
"""Unit tests for validators.email, written by Atifa Saqib.

Techniques: ECP (valid and invalid format classes) and BVA (username length
limit of 64 and domain length limit of 253).
Tests marked "predicted" come from reading the source code and are confirmed
by running them.
"""
import pytest

from validators import ValidationError, email

pytestmark = pytest.mark.group_email


def make_username(size):
    """Build a username with exactly `size` characters."""
    return "u" * size


def make_domain(total):
    """Build a domain with exactly `total` characters (valid label sizes)."""
    labels = ["a" * 63, "a" * 63, "a" * 63, "b" * (total - 196)]
    return ".".join(labels) + ".com"


# ---------- ECP: valid classes ----------

@pytest.mark.ecp
@pytest.mark.smoke
@pytest.mark.case_order(1)
@pytest.mark.parametrize(
    "address",
    [
        "john.doe@gmail.com",
        "my_name@company.net",
        "12345@example.com",
        "o'brien@example.com",
        "JOHN.DOE@EXAMPLE.ORG",
        "first.middle.last@example.com",
    ],
)
def test_valid_addresses(address):
    """ECP valid classes: each address follows all the rules."""
    assert email(address) is True


# ---------- ECP: invalid classes ----------

@pytest.mark.ecp
@pytest.mark.negative
@pytest.mark.parametrize(
    "address",
    [
        "plainaddress",           # no @
        "a@b@c.com",              # two @
        "name@",                  # missing domain
        "@domain.com",            # missing username
        "na me@example.com",      # space in username
        "name@exam ple.com",      # space in domain
        ".name@example.com",      # dot at the start
        "name.@example.com",      # dot at the end
        "na..me@example.com",     # two dots in a row
        "name(x)@example.com",    # parentheses not allowed
        "na,me@example.com",      # comma not allowed
        "name@example",           # no top-level domain
        "name@.example.com",      # domain starts with a dot
        "name@example..com",      # two dots in the domain
        "name@-example.com",      # label starts with a hyphen
    ],
)
def test_invalid_addresses(address):
    """ECP invalid classes: each address breaks one rule."""
    assert isinstance(email(address), ValidationError)


@pytest.mark.ecp
@pytest.mark.negative
@pytest.mark.parametrize("address", ["", "   ", None])
def test_empty_blank_or_missing(address):
    """ECP invalid class: empty, spaces only and None are rejected."""
    assert isinstance(email(address), ValidationError)


# ---------- BVA: username length (maximum 64) ----------

@pytest.mark.bva
@pytest.mark.parametrize(
    ("size", "expected_ok"),
    [
        (1, True),
        (2, True),
        (63, True),
        (64, True),    # exactly the limit
        (65, False),   # just above the limit
    ],
)
def test_username_length_boundaries(size, expected_ok):
    """BVA: usernames up to 64 characters pass, 65 fails."""
    result = email(make_username(size) + "@example.com")
    assert (result is True) == expected_ok


# ---------- BVA: domain length (maximum 253) ----------

@pytest.mark.bva
def test_domain_length_just_above_limit():
    """BVA: a 254-character domain is rejected by the length check."""
    assert len(make_domain(254)) == 254
    assert isinstance(email("user@" + make_domain(254)), ValidationError)


@pytest.mark.bva
def test_domain_length_at_limit():
    """BVA predicted: a 253-character domain with valid labels passes."""
    assert len(make_domain(253)) == 253
    assert email("user@" + make_domain(253)) is True


# ---------- Optional flags ----------

@pytest.mark.ecp
def test_simple_host_flag():
    """A host with no dot is rejected unless simple_host=True."""
    assert isinstance(email("admin@intranet"), ValidationError)
    assert email("admin@intranet", simple_host=True) is True


@pytest.mark.ecp
def test_ipv4_domain():
    """predicted: an IPv4 domain needs [brackets] and ipv4_address=True."""
    assert email("user@[10.0.0.1]", ipv4_address=True) is True
    assert isinstance(email("user@10.0.0.1", ipv4_address=True), ValidationError)
    assert isinstance(email("user@[10.0.0.1]"), ValidationError)


@pytest.mark.ecp
def test_ipv6_domain():
    """predicted: an IPv6 domain needs [brackets] and ipv6_address=True."""
    assert email("user@[2001:db8::2]", ipv6_address=True) is True
    assert isinstance(email("user@2001:db8::2", ipv6_address=True), ValidationError)
