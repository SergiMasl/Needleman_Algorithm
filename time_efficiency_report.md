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

## Optimizations Applied (2026-04-02)

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

## Remaining Bottleneck

The inner loop over the matrix is still a pure Python `for` loop. Full vectorization of the NW recurrence is not possible in the standard approach because each cell depends on its diagonal, upper, and left neighbors (sequential data dependency).

For sequences longer than ~2,000 bases, this loop will remain slow. Future options if needed:

| Approach | Benefit | Cost |
|---|---|---|
| `numba` JIT (`@njit`) | 10–100× speedup on the loop | New dependency |
| Anti-diagonal vectorization | Full NumPy, no new deps | Complex to implement |
| `Biopython` pairwise aligner | Highly optimized C backend | Major dependency |

---

## Summary

| Optimization | Estimated Speedup |
|---|---|
| Remove duplicate matrix fill | ~2× |
| NumPy border init | Minor |
| Precomputed diagonal scores | Moderate (scales with sequence length) |
| **Total** | **~2–3× over original** |
