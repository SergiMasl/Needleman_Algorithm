# Error Handling Report

**Project:** Needleman-Wunsch Alignment
**Date:** 2026-04-29

---

## Overview

This document catalogues all error handling present in the project, organized by module. Each entry describes the condition being caught, the exception type raised, and the message surfaced to the caller.

---

## `modules/parsing_lib/get_scoring_parameters.py`

### `get_scoring_parameters() -> Tuple[int, int, int]`

| Condition | Exception | Message |
|-----------|-----------|---------|
| User enters a non-integer match score | `ValueError` | `"Match score must be an integer."` |
| User enters a non-integer mismatch score | `ValueError` | `"Mismatch score must be an integer."` |
| User enters a non-integer gap penalty | `ValueError` | `"Gap penalty must be an integer."` |

**Notes:**
- Invalid yes/no input is handled with a `while` loop re-prompt rather than an exception — no crash possible here.
- Default values (`match=2`, `mismatch=-1`, `gap=-2`) are used when the user selects `yes`.

---

## `modules/parsing_lib/parsing.py`

### `parsing(file_from_input, match_score, mismatch_score, gap_penalty)`

| Condition | Exception | Message |
|-----------|-----------|---------|
| `file_from_input` is missing `.seq_a` or `.seq_b` | `AttributeError` | `"Input object is missing sequence data: <original error>"` |
| Matrix dimensions are invalid (e.g. zero-length sequence) | `ValueError` | `"Could not allocate scoring matrix (<rows>x<cols>): <original error>"` |
| Sequences are not ASCII-encodable strings | `ValueError` | `"Sequences must be ASCII strings: <original error>"` |
| Display grid construction fails | `RuntimeError` | `"Failed to construct display grid: <original error>"` |

**Notes:**
- Scoring parameters are validated upstream in `get_scoring_parameters()` before reaching this function.
- Matrix border initialization uses NumPy slicing; dimension errors are caught at allocation time.

---

## `modules/report_lib/report.py`

### `traceback_graphing(matrix, seq_a, seq_b, match, mismatch, gap, tie_point)`

| Condition | Exception | Message |
|-----------|-----------|---------|
| `matrix` is not a 2D NumPy array | `TypeError` | `"matrix must be a 2D numpy array"` |
| `seq_a` is empty or not a string | `ValueError` | `"seq_a must be a non-empty string"` |
| `seq_b` is empty or not a string | `ValueError` | `"seq_b must be a non-empty string"` |
| `tie_point` coordinates fall outside matrix bounds | `IndexError` | `"tie_point <coords> is out of matrix bounds (<rows>x<cols>)"` |

---

### `report(matrix, seq_a, seq_b, match, mismatch, gap, output_path, tie_point)`

| Condition | Exception | Message |
|-----------|-----------|---------|
| `matrix` is not a 2D NumPy array | `TypeError` | `"matrix must be a 2D numpy array"` |
| `seq_a` is empty or not a string | `ValueError` | `"seq_a must be a non-empty string"` |
| `seq_b` is empty or not a string | `ValueError` | `"seq_b must be a non-empty string"` |
| `matrix.shape` does not match `(len(seq_b)+1, len(seq_a)+1)` | `ValueError` | `"matrix shape <actual> does not match expected <expected> for seq_a length <n> and seq_b length <m>"` |
| `tie_point` coordinates fall outside matrix bounds | `IndexError` | `"tie_point <coords> is out of matrix bounds (<rows>x<cols>)"` |
| User-provided `output_path` parent directory cannot be created | `OSError` | `"Cannot create output directory '<path>': <original error>"` |
| Writing figures to PDF fails (disk full, permissions, etc.) | `RuntimeError` | `"Failed to write PDF report to '<path>': <original error>"` |

**Figure cleanup guarantee:**
All Matplotlib figures (`fig`, `fig2`, `fig3`) are initialized to `None` before any plot is created. A `try/finally` block ensures `plt.close()` is called on every open figure regardless of whether the PDF write succeeded or failed, preventing memory leaks.

---

## `main.py`

### `CreateAlignment.main()`

No internal try/except — exceptions propagate to the top-level guard below.

### Top-level guard (`__main__`)

| Condition | Behaviour |
|-----------|-----------|
| `ValueError`, `TypeError`, `AttributeError`, `IndexError`, `OSError`, `RuntimeError` | Prints `Error: <message>` and exits with code `1` |
| Any other unexpected exception | Prints `Unexpected error: <message>` and exits with code `1` |
| Either outcome (success or failure) | `__pycache__` directories are always cleaned up via `finally` |

---

## Error Propagation Chain

```
main.py  (top-level try/except → clean exit message)
  └── input_sequences()
  └── parsing()
        └── get_scoring_parameters()   ← ValueError on bad int input
        └── matrix allocation          ← ValueError / AttributeError
        └── GridBuild.matrix_construct ← RuntimeError
  └── report()
        ├── Input validation           ← TypeError / ValueError / IndexError
        ├── Output directory creation  ← OSError
        ├── traceback_graphing()       ← TypeError / ValueError / IndexError
        └── PdfPages write             ← RuntimeError (wraps any I/O failure)
              finally: plt.close() on all figures
```

---

## What Is Not Handled (Known Limitations)

| Scenario | Current Behaviour |
|----------|-------------------|
| Sequences containing non-DNA characters (e.g. spaces, digits) | Accepted silently; scoring still runs but biological meaning is undefined |
| Very large sequences causing excessive memory use | No size cap; NumPy allocation may raise `MemoryError` uncaught |
| `tie_point` of `(0, 0)` passed to `traceback_graphing` | Bounds check passes; traceback terminates immediately at origin with only that cell in path — may not be meaningful |
| `output_path` points to an existing file with no write permission | `RuntimeError` is raised with the OS message, which is sufficient |
