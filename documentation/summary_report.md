# Summary Report - Assignment 3: Unit Test Automation

**Group members:** Amna Wahab, Atifa Saqib
**Project:** validators (open-source Python library for data validation)
**Repository:** https://github.com/code-nomad221/validators-unit-testing

## 1. Setup (Task 1)
The validators project was copied into the group repository. We created a virtual environment, installed the project with `pip install -e ".[crypto-eth-addresses]"`, installed pytest and pytest-xdist, and ran the original test suite. Both members recorded a setup video:
- documentation/setup_video_amna.mp4 (Amna)
- documentation/setup_video_atifa.mp4 (Atifa)

## 2. Modules tested (Task 2)
We tested three modules: between, length and email. Each member wrote her own ECP/BVA notes and tests.

| Member | Notes file | Test files |
|---|---|---|
| Amna | documentation/notes_amna.md | tests/test_between_amna.py, test_length_amna.py, test_email_amna.py |
| Atifa | documentation/notes_atifa.md | tests/test_between_atifa.py, test_length_atifa.py, test_email_atifa.py |

Number of automated tests (Atifa): between 22, length 23, email 34, CSV 12 (91 in total).
Number of automated tests (Amna): between 19, length 20, email 24, CSV 11.

Techniques used: Equivalence Class Partitioning (valid and invalid input classes) and Boundary Value Analysis (values at and around each limit, such as lengths 4, 5, 12 and 13 for a range of 5 to 12).

### Findings
- The documentation of between says it raises ValueError and TypeError, but the @validator wrapper returns a ValidationError instead. Our tests record the real behaviour. The same applies to negative limits in length.

## 3. Test cases and external data (Task 3)

| Member | CSV data file | Data-driven test | Excel sheet |
|---|---|---|---|
| Amna | tests/data/email_test_data_amna.csv | tests/test_email_csv_amna.py | documentation/test_cases_amna.xlsx |
| Atifa | tests/data/length_test_data_atifa.csv | tests/test_length_csv_atifa.py | documentation/test_cases_atifa.xlsx |

Adding a row to a CSV file creates a new test case without any code change.

## 4. Configuration (Task 4)
- Groups: pytest markers group_between, group_length, group_email, group_csv, plus ecp, bva, negative and smoke, registered in tests/conftest.py.
- Execution order: conftest.py sorts tests by group, then by case_order(n) inside a group.
- Suites: selected with `pytest -m`, for example `pytest tests -m bva`.
- Parallel runs: `pytest tests -n auto` (pytest-xdist).
- Parameterization: @pytest.mark.parametrize in all test files and the CSV tests.
- Full commands: documentation/RUN_TESTS_atifa.md.

## 5. Results
All tests pass: 1278 passed in 2.43s (1113 original project tests, 74 tests by Amna and 91 tests by Atifa), including a parallel run with `pytest tests -n auto`.

## 6. Work distribution
Each member worked in her own files, and the Git commit history shows each member's commits.