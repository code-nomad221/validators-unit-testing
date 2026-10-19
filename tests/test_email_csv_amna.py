# pyright: basic
"""Data-driven tests for validators.email, written by Amna Wahab.

Test data is read from an external CSV file (tests/data/email_test_data_amna.csv),
so cases can be added or changed without editing this code.
"""
import csv
from pathlib import Path

import pytest

from validators import ValidationError, email

DATA_FILE = Path(__file__).parent / "data" / "email_test_data_amna.csv"


def load_cases():
    """Read every row of the CSV file as (test_id, email, expected)."""
    with open(DATA_FILE, newline="", encoding="utf-8") as csv_file:
        return [
            (row["test_id"], row["email"], row["expected"])
            for row in csv.DictReader(csv_file)
        ]


CASES = load_cases()


@pytest.mark.parametrize(
    ("test_id", "address", "expected"),
    CASES,
    ids=[case[0] for case in CASES],
)
def test_email_from_csv(test_id, address, expected):
    """Each CSV row becomes one test case."""
    result = email(address)
    if expected == "valid":
        assert result is True
    else:
        assert isinstance(result, ValidationError)