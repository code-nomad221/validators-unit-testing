# Test Design Notes - Amna Wahab

## Module 1: between (src/validators/between.py)

### Function: between(value, min_val=None, max_val=None)
Checks that value is within min_val and max_val (both inclusive).

### ECP (Equivalence Class Partitioning), with min=10, max=20
| Class | Sample value | Expected |
|---|---|---|
| Inside range | 15 | True |
| Below range | 3 | ValidationError |
| Above range | 50 | ValidationError |
| Only min given | 5 with min 2 | True |
| Only max given | 500 with max 400 | ValidationError |
| No limits | 7 | True |
| value is None | None | ValidationError |
| min greater than max | min 20, max 10 | ValueError |
| Type mismatch | "abc" with min 10 | TypeError |
| Float / date / text | 13.2 in 13 to 14 | True |

### BVA (Boundary Value Analysis), with min=10, max=20
| Value | Meaning | Expected |
|---|---|---|
| 9 | just below min | ValidationError |
| 10 | min | True |
| 11 | just above min | True |
| 19 | just below max | True |
| 20 | max | True |
| 21 | just above max | ValidationError |
| 10 with min=10, max=10 | min equals max | True |