# Physics check — the V10 variance criterion, 2026-09-09

Checked by the planning model before the gate, because R8(b) is the one C0 row
whose correctness is a statistics question rather than a coding question.

## What the criterion has to be

Each repeat draws N_kept post-selected shots from the same pooled codeword
distribution. An observable O takes a fixed value o_k on codeword k, so a single
shot has variance

    Var_s = sum_k p_k o_k^2 - (sum_k p_k o_k)^2

and the mean over R repeats of N_kept shots each has standard error
sqrt(Var_s / (R * N_kept)). A bootstrap over R resampled repeats underestimates
that by sqrt((R - 1) / R), which is 0.894 at R = 5. The acceptance therefore
compares two_sigma / 2 against 0.894 * sqrt(Var_s / (5 * N_kept_mean)) and
requires the ratio to sit inside a factor of two.

## What the test computes

The per-codeword values o_k are obtained by evaluating the observable function
on a one-element sample, which returns exactly the o_k vector because the
function accumulates weight times value. The pooled kept counts across the five
repeats supply p_k. The variance is then formed as written above and clamped at
zero to absorb round-off. This is the right quantity, computed from measured
data rather than from a model of it.

Two details are correct and worth recording:

- The constant offset in `dC` cancels in a variance, so evaluating it this way
  is legitimate.
- Observables with Var_s = 0 are structurally empty, meaning the channel is
  unoccupied in the pooled sample. They are listed and skipped rather than
  counted as failures, and they are explicitly not treated as evidence that the
  twin is deterministic. That distinction is what the old `any(two_sigma > 0)`
  criterion lost.

## Verdict

The criterion as implemented is the correct multinomial prediction and the
factor-two band is applied to every observable that has a nonzero prediction.
Approved for the gate.
