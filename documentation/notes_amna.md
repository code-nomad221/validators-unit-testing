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

### Finding
The docstring says `between` raises ValueError (min > max) and TypeError
(type mismatch), but the `@validator` decorator catches these and returns
a ValidationError instead. Tests assert the actual behaviour.

## Module 2: length (src/validators/length.py)

### Function: length(value, min_val=None, max_val=None)
Checks that len(value) is within min_val and max_val (both inclusive).
It calls between() on the length. Negative limits raise ValueError.

### ECP, with min=3, max=8
| Class | Sample | Expected |
|---|---|---|
| Length inside range | "abcde" | True |
| Length below range | "ab" | ValidationError |
| Length above range | "abcdefghijkl" | ValidationError |
| Only min given | "something", min 2 | True |
| Only max given | "something", max 5 | ValidationError |
| No limits | "abc" | True |
| Empty string, no limits | "" | True |
| Empty string, min 1 | "" | ValidationError |
| Negative limit | min -1 | ValidationError (wrapper) |
| Reversed limits | min 8, max 3 | ValidationError (wrapper) |
| Wrong type | 12345 | ValidationError (wrapper) |

### BVA, with min=3, max=8
| Length | Meaning | Expected |
|---|---|---|
| 2 | just below min | ValidationError |
| 3 | min | True |
| 4 | just above min | True |
| 7 | just below max | True |
| 8 | max | True |
| 9 | just above max | ValidationError |
| 0 with min_val=0 | lowest allowed limit | True |

## Module 3: email (src/validators/email.py)

### Function: email(value, ipv4_address, ipv6_address, simple_host, rfc_1034, rfc_2782)
Rejects empty values and anything without exactly one @. Username max 64
characters, domain max 253. Username is checked with a regex (dots only
between characters, no spaces). Domain is checked by the hostname validator.

### ECP
| Class | Sample | Expected |
|---|---|---|
| Plain valid | user@example.com | True |
| Dot in username | first.last@example.com | True |
| Plus tag | user+tag@example.com | True |
| Subdomain | user@sub.example.com | True |
| No @ | userexample.com | ValidationError |
| Two @ | user@@example.com | ValidationError |
| Missing domain | user@ | ValidationError |
| Missing username | @example.com | ValidationError |
| Space in username | user name@example.com | ValidationError |
| Misplaced dots | .user@ / user.@ / us..er@ | ValidationError |
| No top-level domain | user@example | ValidationError |
| Empty / None | "" / None | ValidationError |
| simple_host flag | user@localhost | True only with flag |
| IP in brackets | user@[192.168.1.1] | True only with flag |
| Trailing dot | user@example.com. | True only with rfc_1034 |

### BVA (username length, max 64)
| Length | Expected |
|---|---|
| 1, 63, 64 | True |
| 65 | ValidationError |

The domain length limit (253) is not tested because a valid 253-character
domain is hard to build within the per-label limits.