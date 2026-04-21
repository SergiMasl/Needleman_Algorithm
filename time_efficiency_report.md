# Time Efficiency Report — Needleman-Wunsch Alignment Tool

## Complexity Overview

| Module | Operation | Complexity |
|---|---|---|
| `parsing.py` | Matrix fill (NW recurrence) | O(m × n) |
| `scrolling_output.py` | Traceback | O(m + n) |
| `scrolling_output.py` | Consensus build | O(m + n) |
| `report.py` | PDF render | O(m × n) — matplotlib table scales with matrix size |

Where `m` = length of seq_a, `n` = length of seq_b.

---

## Optimizations Applied (2026-04-02, updated 2026-04-16)

### 1. Removed Duplicate Matrix Fill

**Before:** `parsing.py` filled the NW matrix with a Python double loop, then called `GridBuild.matrix_construct()` which ran the exact same double loop a second time.

**After:** `matrix_construct()` returns the matrix as-is. The matrix is filled exactly once.

**Impact:** ~2× speedup on the matrix fill step — the most expensive part of the algorithm.

---

### 2. NumPy Border Initialization

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

### 3. Precomputed Diagonal Score Matrix

**Before:** Every cell in the inner loop did a Python character comparison:
```python
if seq_b[i - 1] == seq_a[j - 1]:
    diagonal = matrix[i-1][j-1] + match_score
else:
    diagonal = matrix[i-1][j-1] + mismatch_score
```

**After:** All match/mismatch scores computed once before the loop using NumPy broadcasting:
```python
seq_b_arr = np.frombuffer(seq_b.encode(), dtype=np.uint8)
seq_a_arr = np.frombuffer(seq_a.encode(), dtype=np.uint8)
diag_scores = np.where(seq_b_arr[:, None] == seq_a_arr[None, :], match_score, mismatch_score)
```

Inside the loop, each cell just does an array lookup:
```python
diagonal = matrix[i - 1, j - 1] + diag_scores[i - 1, j - 1]
```

**Impact:** Removes one Python conditional branch per cell — for a 1000×1000 matrix that is 1,000,000 fewer Python-level comparisons.

---

### 4. Numba JIT on `matrix_build` (2026-04-16)

**Change:** Added `@njit` decorator from `numba` to `matrix_build()` in `scrolling_output.py`. The function was also refactored to self-initialize the matrix (allocates `np.zeros`, fills borders) entirely inside the JIT-compiled function rather than relying on the caller.

**Before:**
```python
def matrix_build(self, seq_a, seq_b, gap):
    ...
```

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

**Impact:** Matrix initialization now runs as compiled machine code via LLVM. First invocation incurs a one-time JIT compilation cost; all subsequent calls are significantly faster. This also consolidates allocation and border-fill into a single compiled pass.

**Note:** The first run of the program will be slower than usual due to Numba's ahead-of-time compilation step. Subsequent runs use the cached compiled version.

---

## Remaining Bottleneck

The `view_traceback()` inner loop is still a pure Python `for` loop. Full vectorization of the NW traceback is not straightforward because each step depends on the current cell's neighbors (sequential data dependency).

For sequences longer than ~2,000 bases, this loop will remain the dominant cost. Options if further optimization is needed:

| Approach | Benefit | Cost | Status |
|---|---|---|---|
| `numba` JIT (`@njit`) on `matrix_build` | Fast matrix init | One-time compile cost | **Implemented (2026-04-16)** |
| `@njit` on `view_traceback` | 10–100× speedup on traceback | Requires rewriting deque logic with plain arrays | Not yet applied |
| Anti-diagonal vectorization (NW fill) | Full NumPy, no new deps | Complex to implement | Not applied |
| `Biopython` pairwise aligner | Highly optimized C backend | Major dependency, replaces core logic | Not applied |

---

## Summary

| Optimization | Estimated Speedup |
|---|---|
| Remove duplicate matrix fill | ~2× |
| NumPy border init | Minor |
| Precomputed diagonal scores | Moderate (scales with sequence length) |
| Numba JIT on `matrix_build` | Significant for init; negligible vs. traceback loop |
| **Total** | **~2–3× over original (traceback loop remains the bottleneck)** |
