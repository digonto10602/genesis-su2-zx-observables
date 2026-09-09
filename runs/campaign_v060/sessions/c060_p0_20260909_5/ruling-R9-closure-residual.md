# Ruling — the R9 violating-input row, 2026-09-09

## The question

R9 requires `channel_closure_residual` to return the correct nonzero residual on
an input deliberately built to violate the identity through an unphysical key
that `l12.decode` rejects. Two sessions have now recorded that this is
unsatisfiable against the implementation: `channel_weights` and the right-hand
side of the residual both skip keys that fail to decode, so such a key
contributes zero to both sides. Measured on the row-1 synthetic input with an
unphysical key carrying weight 0.37, the residual is
-1.1102230246251565e-16 with and without the key, bit for bit.

## What the identity actually says

The left-hand side is the sum of the four channel totals over decodable keys.
The right-hand side is the weight carried by keys with N = 4, plus the weight of
keys with N != 4 that have some |q_v| = 2, again over decodable keys. Both sides
range over the same decodable set, so a key that decodes to nothing genuinely
perturbs neither. The identity is a statement about the completeness of the
channel decomposition of the physical weight. It is not, as written, a validator
of the input.

`kept` is by contract the output of `postselect`, which admits only physical
codes. An undecodable key in `kept` is therefore an upstream contract violation,
and R9 is right that the gate must be able to see it. The defect is that the
residual currently cannot.

## Ruling

The right-hand side gains one term: the total weight of keys that fail to
decode. Nothing else changes.

    residual = sum(four channel totals)
             - [ W(N = 4) + W(N != 4 and some |q_v| = 2) + W(undecodable) ]

Consequences, all checked:

- On any contract-satisfying input, every key decodes, the new term is
  identically zero, and the residual is bit-for-bit what it is today. No gated
  number, no channel definition, no threshold and no observable changes.
- On the violating input the residual becomes -0.37, whose magnitude is exactly
  the injected weight, which is what R9 demands.
- A decodable key that falls in no channel, such as an N != 4 codeword with no
  |q_v| = 2, stays outside both sides. It must: it is legitimate physical weight
  that the four channels do not claim, and folding it into the right-hand side
  would break the identity on honest input.

The alternative of raising on an undecodable key was rejected: it converts a
measurement into a validator and would change the behaviour of callers that
legitimately hand in unfiltered counts. The alternative of summing all kept
weight into the right-hand side without restricting the new term to undecodable
keys was rejected because it breaks the identity on the no-channel codeword.

## Consequence for the test

`test_row2_violating_input_must_give_the_correct_nonzero_residual` was written
with a strict xfail carrying this reason, so that it would fail loudly rather
than rot once the module was repaired. With this ruling applied the xfail is
removed and the row is asserted outright.
