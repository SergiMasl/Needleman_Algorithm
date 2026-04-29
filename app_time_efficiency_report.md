# Time Efficiency Report — Needleman-Wunsch Alignment Tool

## Complexity Overview

| Module | Operation | Complexity |
|---|---|---|
| `validation.py` | DNA character validation | O(n) — single pass over sequence |
| `input.py` | FASTA file read | O(n) — line-by-line read |
| `parsing.py` | Matrix allocation + border init | O(m × n) allocation, O(m + n) border fill |
| `parsing.py` | Diagonal score precomputation | O(m × n) — broadcasting over full matrix |
| `parsing.py` | NW matrix fill (inner loop) | O(m × n) |
| `scrolling_output.py` | `find_ties` — tie detection scan | O(m + n) — single traceback scan |
| `scrolling_output.py` | `view_traceback` — primary alignment | O(m + n) |
| `scrolling_output.py` | `tie_traceback` — alternate alignment | O(m + n) — only when a tie exists |
| `scrolling_output.py` | `build_consensus` | O(m + n) — one pass over aligned sequences |
| `report.py` | `_gc_content` | O(n) per sequence |
| `report.py` | PDF render (matrix table) | O(m × n) — matplotlib table scales with matrix size |
| `report.py` | PDF render (alt traceback page) | O(m × n) — only rendered when a tie exists |

Where `m` = length of seq_a, `n` = length of seq_b.

---

## Optimizations Applied

### 1. Removed Duplicate Matrix Fill (2026-04-02)

**Before:** `parsing.py` filled the NW matrix with a Python double loop, then called `GridBuild.matrix_construct()` which ran the exact same double loop a second time.

**After:** `matrix_construct()` returns the matrix as-is. The matrix is filled exactly once.

**Impact:** ~2× speedup on the matrix fill step — the most expensive part of the algorithm.

---

### 2. NumPy Border Initialization (2026-04-02)

**Before:**
```python
for i in range(1, rows):
    matrix[i][0] = i * gap_penalty
for j in range(1, cols):
    matrix[0][j] = j * gap_penalty
```

**After:**
```python
matrix[1:, 0] = np.arange(1, rows) * gap_penalty
matrix[0, 1:] = np.arange(1, cols) * gap_penalty
```

**Impact:** Border initialization moved from interpreted Python loops to NumPy C-level operations.

---

### 3. Precomputed Diagonal Score Array (2026-04-02)

**Before:** Every cell in the inner loop did a Python character comparison:
```python
if seq_b[i - 1] == seq_a[j - 1]:
    diagonal = matrix[i-1][j-1] + match_score
else:
    diagonal = matrix[i-1][j-1] + mismatch_score
```

**After:** Sequences are encoded to byte arrays and a score matrix is computed once before the loop:
```python
seq_b_arr = np.frombuffer(seq_b.encode(), dtype=np.uint8)
seq_a_arr = np.frombuffer(seq_a.encode(), dtype=np.uint8)
char_score = np.vectorize(lambda b, a: match_score if b == a else mismatch_score)
diag_scores = char_score(seq_b_arr[:, None], seq_a_arr[None, :])
```

Inside the loop, each cell does an array lookup instead of a character comparison:
```python
diagonal = matrix[i - 1, j - 1] + diag_scores[i - 1, j - 1]
```

**Impact:** Eliminates the Python conditional branch from the hot inner loop. For a 1000×1000 matrix, that is 1,000,000 fewer Python-level comparisons during fill.

**Known limitation:** `np.vectorize` is documented as a convenience wrapper, not a performance tool — it still calls the lambda once per element in Python. The precomputation step itself is not fully vectorized. Replacing `np.vectorize` with `np.where` would make the precomputation a true C-level operation:
```python
# More efficient alternative (not yet applied):
diag_scores = np.where(
    seq_b_arr[:, None] == seq_a_arr[None, :],
    match_score,
    mismatch_score
)
```

---

### 4. Numba JIT on `matrix_build` (2026-04-16)

**Change:** Added `@njit` decorator from `numba` to `matrix_build()` in `scrolling_output.py`. The function allocates `np.zeros`, fills both borders, and returns the matrix entirely inside the JIT-compiled function.

**After:**
```python
from numba import njit

@njit
def matrix_build(seq_a, seq_b, gap):
    rows = len(seq_a) + 1
    cols = len(seq_b) + 1
    matrix = np.zeros((rows, cols), dtype=np.int32)
    matrix[:, 0] = np.arange(rows) * gap
    matrix[0, :] = np.arange(cols) * gap
    return matrix
```

**Impact:** Matrix initialization now runs as compiled machine code via LLVM. First invocation incurs a one-time JIT compilation cost; all subsequent calls are significantly faster. Allocation and border-fill are consolidated into a single compiled pass.

**Note:** The first run of the program will be slower than usual due to Numba's ahead-of-time compilation step. Subsequent runs use the cached compiled version.

---

### 5. `deque` for Traceback Sequence Building (2026-04-12)

**Change:** `view_traceback()` and `tie_traceback()` in `scrolling_output.py` use `collections.deque` for `seq_align_a` and `seq_align_b` instead of plain lists.

**Impact:** `deque.appendleft()` is O(1). The equivalent on a plain list — `list.insert(0, x)` — is O(n) because it shifts every existing element. For a traceback of length L, this reduces sequence-building from O(L²) to O(L).

---

## New Functionality — Performance Notes (2026-04-12)

### Tie Detection and Alternate Traceback

Two additional O(m + n) passes are now performed when an alternate optimal alignment exists:

- **`find_ties()`** — scans from the bottom-right corner to the top-left, looking for the first cell where more than one optimal move is valid. Returns `(row, col)` of the tie point or `None`.
- **`tie_traceback()`** — if a tie is found, traces the alternate alignment path from the tie point, resolving the branch differently from the primary path.

When a tie is present, `report.py` also generates a third PDF page with the alternate traceback highlighted. This adds a full second O(m × n) matplotlib table render to the reporting step.

**Net cost of tie handling:** Two extra O(m + n) passes and one extra O(m × n) PDF render, incurred only when at least one tie cell exists in the matrix.

---

## Remaining Bottlenecks

### NW Inner Fill Loop

The matrix fill in `parsing.py` is still a pure Python `for` loop over rows and columns. Each cell's `max(diagonal, up, left)` depends on cells immediately above and to the left — a sequential data dependency that prevents straightforward vectorization of the fill step itself.

For sequences longer than ~2,000 bases, this double loop is the dominant cost.

### Diagonal Score Precomputation

As noted in Optimization #3, `np.vectorize` does not provide true vectorization. For large sequences, replacing it with `np.where` would give a meaningful speedup on the precomputation step at no cost.

---

## Optimization Roadmap

| Approach | Benefit | Cost | Status |
|---|---|---|---|
| NumPy border init | Fast O(m+n) border fill | — | **Implemented** |
| Precomputed diagonal scores (vectorize) | Removes branch from inner loop | Precompute step is still slow | **Implemented** |
| `deque` for traceback building | O(L) vs O(L²) sequence assembly | — | **Implemented** |
| Numba JIT on `matrix_build` | Fast matrix init | One-time compile cost | **Implemented (2026-04-16)** |
| Replace `np.vectorize` → `np.where` | True vectorization of precompute | Trivial change | **Not yet applied** |
| `@njit` on `view_traceback` | 10–100× speedup on traceback | Requires rewriting `deque` logic with plain arrays | Not yet applied |
| Anti-diagonal vectorization (NW fill) | Fully vectorized matrix fill | Complex to implement; requires restructuring fill loop | Not applied |
| `Biopython` pairwise aligner | Highly optimized C backend | Major dependency, replaces core logic | Not applied |

---

## Summary

| Optimization | Estimated Speedup |
|---|---|
| Remove duplicate matrix fill | ~2× |
| NumPy border init | Minor |
| Precomputed diagonal scores | Moderate for fill; precompute step itself still O(m×n) via `np.vectorize` |
| `deque` in traceback | Significant for long sequences (O(L) vs O(L²)) |
| Numba JIT on `matrix_build` | Significant for init; minor vs. fill loop cost |
| **Total** | **~2–3× over original — fill loop and `np.vectorize` precompute remain the primary bottlenecks** |
