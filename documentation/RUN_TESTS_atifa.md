# How to run the tests (Atifa Saqib)

## Setup
```
.venv\Scripts\activate
pip install -e ".[crypto-eth-addresses]"
pip install pytest pytest-xdist
```

## Groups (pytest markers, registered in tests/conftest.py)

| Marker | Meaning |
|---|---|
| group_between / group_length / group_email / group_csv | One group per module (the CSV group holds the data-driven tests) |
| ecp | Tests from equivalence class partitioning |
| bva | Tests from boundary value analysis |
| negative | Tests with invalid input |
| smoke | One quick basic test per module |
| case_order(n) | Order of a test inside its group |

## Execution order
tests/conftest.py sorts tests by group: between, length, email, csv. Inside a group, tests with case_order(n) run first, in number order.

## Suites (commands)

| Suite | Command |
|---|---|
| My tests, in order | `pytest tests\test_between_atifa.py tests\test_length_atifa.py tests\test_email_atifa.py tests\test_length_csv_atifa.py -v` |
| Smoke suite | `pytest tests -m smoke -v` |
| Boundary suite | `pytest tests -m bva -v` |
| Equivalence class suite | `pytest tests -m ecp -v` |
| Negative suite | `pytest tests -m negative -v` |
| One module | `pytest tests -m group_length -v` |
| Two modules | `pytest tests -m "group_between or group_length" -v` |
| Combined filter | `pytest tests -m "group_email and negative" -v` |
| Data-driven tests | `pytest tests\test_length_csv_atifa.py -v` |

## Parallel runs
`pytest tests -n auto` runs the tests on all CPU cores. `pytest tests -n 2` uses 2 workers. Order is only guaranteed without -n.

## Parameterization
Tests use @pytest.mark.parametrize. The CSV test reads tests/data/length_test_data_atifa.csv, so a new CSV row creates a new test without changing code.