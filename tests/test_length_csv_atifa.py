# pyright: basic
"""Data-driven tests for validators.length, written by Atifa Saqib.

The test data comes from an external CSV file
(tests/data/length_test_data_atifa.csv), so cases can be added or changed
without editing this code.
"""
import csv
from pathlib import Path

import pytest

from validators import ValidationError, length

pytestmark = pytest.mark.group_csv

DATA_FILE = Path(__file__).parent / "data" / "length_test_data_atifa.csv"


def to_limit(cell):
    """An empty CSV cell means 'no limit' (None); otherwise a whole number."""
    return int(cell) if cell != "" else None


def load_cases():
    """Read every CSV row as (test_id, text, min_val, max_val, expected)."""
    with open(DATA_FILE, newline="", encoding="utf-8") as csv_file:
        return [
            (
                row["test_id"],
                row["text"],
                to_limit(row["min_val"]),
                to_limit(row["max_val"]),
                row["expected"],
            )
            for row in csv.DictReader(csv_file)
        ]


CASES = load_cases()


@pytest.mark.parametrize(
    ("test_id", "text", "min_val", "max_val", "expected"),
    CASES,
    ids=[case[0] for case in CASES],
)
def test_length_from_csv(test_id, text, min_val, max_val, expected):
    """Each CSV row becomes one test case."""
    result = length(text, min_val=min_val, max_val=max_val)
    if expected == "valid":
        assert result is True
    else:
        assert isinstance(result, ValidationError)
