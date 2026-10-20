# Test Design Notes - Atifa Saqib

## Module 1: between (src/validators/between.py)

### Function: between(value, min_val=None, max_val=None)

Checks that value lies within min_val and max_val. Both edges are valid.

### ECP (Equivalence Class Partitioning), range 1 to 100

| Class | Sample value | Expected |
|---|---|---|
| Inside range | 50 | True |
| Below range | -5 | ValidationError |
| Above range | 250 | ValidationError |
| Decimal inside range | 99.5 | True |
| Negative range | -5 in -10 to -1 | True |
| Only min given | 1000 with min 1 | True |
| Only max given | 5 with max 0 | ValidationError |
| No limits | 42 | True |
| Value is None | None | ValidationError |
| Text in range | "mango" between "apple" and "zebra" | True |
| Min greater than max | 50, min 100, max 1 | ValidationError |
| Type mismatch | "abc" with numbers | ValidationError |

### BVA (Boundary Value Analysis), range 1 to 100

| Value | Meaning | Expected |
|---|---|---|
| 0 | just below min | ValidationError |
| 1 | min | True |
| 2 | just above min | True |
| 99 | just below max | True |
| 100 | max | True |
| 101 | just above max | ValidationError |
| 0.99 / 1.0 / 100.01 | decimal edges | ValidationError / True / ValidationError |
| 7 with min=7, max=7 | min equals max | True |