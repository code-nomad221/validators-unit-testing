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


## Module 2: length (src/validators/length.py)

### Function: length(value, min_val=None, max_val=None)

Checks that len(value) lies within min_val and max_val. Both edges are valid. It calls between() on the length. Negative limits are invalid.

### ECP (Equivalence Class Partitioning), length range 5 to 12

| Class | Sample value | Expected |
|---|---|---|
| Length inside range | "hello" (5) / "keyboard" (8) | True |
| Too short | "hi" | ValidationError |
| Too long | "a" * 20 | ValidationError |
| Only min given | "python", min 3 | True |
| Only max given | "python", max 3 | ValidationError |
| No limits | "anything" | True |
| Empty string, no limits | "" | True |
| Empty string, min 1 | "" | ValidationError |
| Spaces count as characters | "     " (5 spaces) | True |
| Non-English letters | "héllo wörld" (11) | True |
| Negative limit | min_val=-1 | ValidationError |
| Reversed limits | min 10, max 2 | ValidationError |
| Number instead of text | 12345 | ValidationError |

### BVA (Boundary Value Analysis), length range 5 to 12

| Length | Meaning | Expected |
|---|---|---|
| 4 | just below min | ValidationError |
| 5 | min | True |
| 6 | just above min | True |
| 11 | just below max | True |
| 12 | max | True |
| 13 | just above max | ValidationError |
| 0 with min_val=0 | lowest allowed limit | True |
| 6 with min=6, max=6 | min equals max | True |

## Module 3: email (src/validators/email.py)

### Function: email(value, ipv4_address, ipv6_address, simple_host, rfc_1034, rfc_2782)

Rejects empty values and anything without exactly one @. The username can be at most 64 characters and the domain at most 253. The username is checked with a pattern (dots only between characters, no spaces). The domain is checked by the hostname validator.

### ECP (Equivalence Class Partitioning)

| Class | Sample value | Expected |
|---|---|---|
| Plain valid | john.doe@gmail.com | True |
| Underscore in username | my_name@company.net | True |
| Digits only username | 12345@example.com | True |
| Apostrophe in username | o'brien@example.com | True |
| Uppercase | JOHN.DOE@EXAMPLE.ORG | True |
| Several dots in username | first.middle.last@example.com | True |
| No @ | plainaddress | ValidationError |
| Two @ | a@b@c.com | ValidationError |
| Missing domain | name@ | ValidationError |
| Missing username | @domain.com | ValidationError |
| Space in username | na me@example.com | ValidationError |
| Space in domain | name@exam ple.com | ValidationError |
| Misplaced dots in username | .name@ / name.@ / na..me@ | ValidationError |
| Illegal symbols in username | name(x)@ / na,me@ / a<b>@ | ValidationError |
| No top-level domain | name@example | ValidationError |
| Dot problems in domain | name@.example.com / name@example..com | ValidationError |
| Hyphen at start of domain label | name@-example.com | ValidationError |
| Empty / None / spaces only | "" / None / "   " | ValidationError |
| simple_host flag | admin@intranet | True only with the flag |
| IPv4 domain | user@[10.0.0.1] | True only with the flag and brackets |
| IPv6 domain | user@[2001:db8::2] | True only with the flag and brackets |

### BVA (Boundary Value Analysis)

| What | Value | Expected |
|---|---|---|
| Username length | 1 | True |
| Username length | 2 | True |
| Username length | 63 | True |
| Username length | 64 (max) | True |
| Username length | 65 | ValidationError |
| Domain length | 253 (max) | True |
| Domain length | 254 | ValidationError |