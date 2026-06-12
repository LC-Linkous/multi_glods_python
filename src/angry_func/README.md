
`angry_func` is function that cannot be solved by multiGLODS (the other optimizers may come up with a default, but not all will)

1. Every initialization point is infeasible. The constraint (X[2] > X[0]/2) or (X[2] < 0.1) → False was inherited from lundquist_3_var, where bounds were [0.21,1]×[0,1]×[0.1,0.5] and the feasible wedge covered most of the box. With angry_func's bounds ([-6,21]×[-6.5,21]×[-6,20]), the feasible region is 0.1 ≤ x₃ ≤ x₀/2 — a thin wedge hugging the x₀ axis that covers only ~15% of the box and excludes the main diagonal entirely. MultiGLODS initializes on the diagonal corners plus the midpoint, and as the test above shows, all four points fail the constraint: the corners have x₃ < 0.1 or x₃ > x₀/2, and the midpoint (7.5, 7.25, 7) has 7 > 3.75. In post_objective_search, one infeasible random point aborts the whole search batch, and ~85% of draws are infeasible.
2. The targets are mathematically unreachable, so it can never converge. TARGETS = [0, 0], but F₁ = (x₂ − 22.2)² wants x₂ = 22.2, which is outside UB = 20 even without the constraint (best unconstrained: 4.84). With the constraint capping x₂ at x₀/2 ≤ 10.5, the minimum possible F₁ is 136.89. F₀ = 0 is reachable (the negative cube can cancel the square), but the L2 norm can never drop below ~136.9, so E_TOL = 1e-15 will never fire and every run grinds to MAXIT or the radius tolerance looking "broken." The Best Eval: 1 in the output is a related cosmetic artifact: the driver initializes best_eval = 1 and only records improvements below it, so for any far-from-target problem it just prints 1 forever.
3. func_F deviates from the suite format. It returns F, noErrors instead of [F], noErrors (multiglods' reshape(-1,1) happens to tolerate it, but other optimizers in the set may not)


To run a function that can be solved:

```python
import numpy as np

def func_F(X, NO_OF_OUTS=2):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        F[0] = (X[0]-21.5) ** 3 + (X[1]+20.1) ** 2
        F[1] = (X[2]-22.2) ** 2
    except Exception as e:
        print(e)
        noErrors = False

    return [F], noErrors

```
