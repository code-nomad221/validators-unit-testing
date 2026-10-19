# How to run the tests - Amna Wahab

## Setup (once)
```
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[crypto-eth-addresses]"
pip install pytest pytest-xdist
```

## Test files
| File | Module | Technique |
|---|---|---|
| tests/test_between_amna.py | between | ECP + BVA |
| tests/test_length_amna.py | length | ECP + BVA |
| tests/test_email_amna.py | email | ECP + BVA |
| tests/test_email_csv_amna.py | email | data-driven, reads tests/data/email_test_data_amna.csv |

## Groups (markers, defined in tests/conftest.py)
| Marker | Meaning |
|---|---|
| group_between, group_length, group_email, group_csv | one group per module / file |
| bva | boundary value tests (cut across the modules) |
| case_order(n) | explicit run order of a test inside its group |

## Execution order
tests/conftest.py sorts the tests: group_between, then group_length, then
group_email, then group_csv. Inside a group, tests marked case_order(n) run
first, in number order. Example: test_min_equals_max runs first.
The order is applied when tests run one after another (the normal run).

## Parameterization
- @pytest.mark.parametrize is used in every file (values and boundaries).
- The CSV file feeds test_email_csv_amna.py: add a row to the CSV to add a test.

## Commands
| What | Command |
|---|---|
| All my tests, in group order | pytest tests/test_between_amna.py tests/test_length_amna.py tests/test_email_amna.py tests/test_email_csv_amna.py -v |
| Parallel run (2 workers) | same files with -n 2 |
| Parallel run (automatic workers) | same files with -n auto |
| Suite: between | pytest tests -m group_between |
| Suite: length | pytest tests -m group_length |
| Suite: email | pytest tests -m group_email |
| Suite: CSV data-driven | pytest tests -m group_csv |
| Suite: boundary values | pytest tests -m bva |
| Everything except boundary tests | pytest tests -m "not bva" |

## Note
With -n (parallel), workers share the tests, so the order across workers
is not guaranteed. Use the normal run to see the group order.