# Error Handling Report

**Project:** Needleman-Wunsch Alignment
**Date:** 2026-04-29

---

## Overview

This document catalogues all error handling present in the project, organized by module. Each entry describes the condition being caught, the exception type raised or action taken, and the message surfaced to the caller or user.

---

## `modules/validation_lib/validation.py`

### `validate_dna_sequence(seq, name) -> str`

| Condition                                         | Exception    | Message                                                                             |
| ------------------------------------------------- | ------------ | ----------------------------------------------------------------------------------- |
| Sequence is empty (after whitespace removal)      | `ValueError` | `"<name> is empty. Please enter a DNA sequence using only A, C, G, and T."`         |
| Sequence contains characters outside {A, C, G, T} | `ValueError` | `"<name> contains invalid character(s): <chars>. Only A, C, G, and T are allowed."` |

**Notes:**

- `normalize_sequence()` is called first — strips whitespace and uppercases before validation. Returns `""` if input is `None` (no exception).

---

### `validate_fasta_loadable(file_path) -> bool`

| Condition                     | Action                                   | Message                              |
| ----------------------------- | ---------------------------------------- | ------------------------------------ |
| File does not exist on disk   | Writes to `stderr`, prompts `retry/exit` | `"[Error] File not found: '<path>'"` |
| File exists but is empty      | Writes to `stderr`, prompts `retry/exit` | `"[Error] File is empty: '<path>'"`  |
| User selects `exit` at prompt | `sys.exit(1)`                            | —                                    |
| User selects `retry`          | Returns `False` (caller re-prompts)      | —                                    |
| File exists and is non-empty  | Returns `True`                           | —                                    |

---

### `validate_fasta_extension(file_path) -> bool`

| Condition                       | Action                              | Message                                                                                   |
| ------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| Path does not end with `.fasta` | Writes to `stderr`, returns `False` | `"[Error] '<path>' is not a .fasta file. Please provide a file with a .fasta extension."` |

---

### `validate_fasta_dna(file_path, raw_seq, label)`

| Condition                                   | Action                                   | Message                                                |
| ------------------------------------------- | ---------------------------------------- | ------------------------------------------------------ |
| `validate_dna_sequence` raises `ValueError` | Writes to `stderr`, prompts `retry/exit` | `"[Error] File '<path>' is invalid: <original error>"` |
| User selects `exit` at prompt               | `sys.exit(1)`                            | —                                                      |
| User selects `retry`                        | Returns `False` (caller re-prompts)      | —                                                      |
| Sequence is valid                           | Returns cleaned uppercase sequence       | —                                                      |

---

### `validate_single_fasta_sequence(file_path)`

| Condition                              | Action                                   | Message                                                                                |
| -------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------- |
| `FileNotFoundError` when opening file  | Returns `True`                           | — (delegated to `parse_fasta_file`)                                                    |
| File contains more than one `>` header | Writes to `stderr`, prompts `retry/exit` | `"[Error] File '<path>' contains <n> sequences. Only 1 sequence per file is allowed."` |
| User selects `exit` at prompt          | `sys.exit(1)`                            | —                                                                                      |
| User selects `retry`                   | Returns `False` (caller re-prompts)      | —                                                                                      |

---

### `validate_int(value, name) -> int`

| Condition                     | Exception    | Message                                             |
| ----------------------------- | ------------ | --------------------------------------------------- |
| Value cannot be cast to `int` | `ValueError` | `"<name> must be an integer. You entered: <value>"` |

---

### `validate_scoring(match, mismatch, gap) -> tuple`

| Condition                        | Exception    | Message                                                          |
| -------------------------------- | ------------ | ---------------------------------------------------------------- |
| All three scoring values are `0` | `ValueError` | `"Scoring cannot be all zeros; alignment would be meaningless."` |

---

## `modules/input_lib/input.py`

### `parse_fasta_file(file) -> tuple | False`

| Condition                  | Action                              | Message                                 |
| -------------------------- | ----------------------------------- | --------------------------------------- |
| File path does not exist   | Writes to `stderr`, returns `False` | `"[Error] Could not find file: <file>"` |
| File is empty (zero lines) | Writes to `stderr`, returns `False` | `"[Error] File is empty: <file>"`       |

**Notes:**

- On success returns `(label, sequence)`. Caller must check for `False` before unpacking.

---

### `read_two_fastas(file1, file2) -> tuple | False`

No direct error handling. Delegates entirely to `parse_fasta_file()` for each file. Returns `False` if either call returns `False`.

---

### `build_sequence_input(raw_a, raw_b, label_a, label_b) -> SequenceInput | False`

| Condition                                                       | Action                              | Message                      |
| --------------------------------------------------------------- | ----------------------------------- | ---------------------------- |
| `validate_dna_sequence` raises `ValueError` for either sequence | Writes to `stderr`, returns `False` | `"[Error] <original error>"` |

---

### `input_sequences(args) -> SequenceInput`

| Condition                                    | Action                                                                            |
| -------------------------------------------- | --------------------------------------------------------------------------------- |
| `fasta` mode — invalid extension             | Calls `validate_fasta_extension()`; continues loop on `False`                     |
| `fasta` mode — file not found or empty       | Calls `validate_fasta_loadable()`; continues loop on `False`                      |
| `fasta` mode — multiple sequences in file    | Calls `validate_single_fasta_sequence()`; continues loop on `False`               |
| `fasta` mode — invalid DNA in file           | Calls `validate_fasta_dna()`; continues loop on `False`                           |
| `manual` mode — invalid DNA sequence entered | Catches `ValueError` from `validate_dna_sequence`, writes to `stderr`, re-prompts |
| `build_sequence_input` returns `False`       | Calls `sys.exit(1)`                                                               |

**Notes:**

- All re-prompting is done with `while True` loops; no exception escapes this function.
- Invalid `fasta`/`manual` choice is handled with a `while` loop — no crash possible.

---

## `modules/parsing_lib/get_scoring_parameters.py`

### `get_scoring_parameters() -> Tuple[int, int, int]`

| Condition                                | Exception    | Message                                |
| ---------------------------------------- | ------------ | -------------------------------------- |
| User enters a non-integer match score    | `ValueError` | `"Match score must be an integer."`    |
| User enters a non-integer mismatch score | `ValueError` | `"Mismatch score must be an integer."` |
| User enters a non-integer gap penalty    | `ValueError` | `"Gap penalty must be an integer."`    |

**Notes:**

- This function is only called from `parsing()` when scoring parameters are not provided via CLI args. In normal CLI usage (`main.py`), scores come from `argparse` and this function is bypassed.
- Invalid yes/no input is handled with a `while` loop re-prompt rather than an exception.
- Default values (`match=2`, `mismatch=-1`, `gap=-2`) are used when the user selects `yes`.

---

## `modules/parsing_lib/parsing.py`

### `parsing(file_from_input, match_score, mismatch_score, gap_penalty)`

| Condition                                                 | Exception        | Message                                                                 |
| --------------------------------------------------------- | ---------------- | ----------------------------------------------------------------------- |
| `file_from_input` is missing `.seq_a` or `.seq_b`         | `AttributeError` | `"Input object is missing sequence data: <original error>"`             |
| Matrix dimensions are invalid (e.g. zero-length sequence) | `ValueError`     | `"Could not allocate scoring matrix (<rows>x<cols>): <original error>"` |
| Sequences are not ASCII-encodable strings                 | `ValueError`     | `"Sequences must be ASCII strings: <original error>"`                   |
| Display grid construction fails                           | `RuntimeError`   | `"Failed to construct display grid: <original error>"`                  |

**Notes:**

- Scoring parameters are validated upstream in `get_scoring_parameters()` before reaching this function (interactive path) or come pre-validated from `argparse` (CLI path).
- Matrix border initialization uses NumPy slicing; dimension errors are caught at allocation time.
- Returns `tie_point` (an `Optional[Tuple[int, int]]`) in addition to the matrix and sequences; callers must unpack all seven values.

---

## `modules/scrolling_output_lib/scrolling_output.py`

### `GridBuild` class — all methods

No explicit `try/except` blocks anywhere in the class. There is no internal error handling in `matrix_build`, `matrix_construct`, `view_traceback`, `find_ties`, `tie_traceback`, or `build_consensus`.

**Notes:**

- `matrix_build` is decorated with `@njit` (Numba JIT); Numba compilation errors would surface at first call, not at import time.
- Any runtime errors (e.g. index out of bounds, type mismatch) propagate unmodified to `parsing()`, which wraps the `matrix_construct` call in a `try/except Exception → RuntimeError`.
- The remaining methods (`view_traceback`, `find_ties`, `tie_traceback`, `build_consensus`) are called directly from `parsing()` or indirectly and are not wrapped — errors would propagate to the top-level guard in `main.py`.

---

## `modules/report_lib/report.py`

### `traceback_graphing(matrix, seq_a, seq_b, match, mismatch, gap, tie_point)`

| Condition                                          | Exception    | Message                                                        |
| -------------------------------------------------- | ------------ | -------------------------------------------------------------- |
| `matrix` is not a 2D NumPy array                   | `TypeError`  | `"matrix must be a 2D numpy array"`                            |
| `seq_a` is empty or not a string                   | `ValueError` | `"seq_a must be a non-empty string"`                           |
| `seq_b` is empty or not a string                   | `ValueError` | `"seq_b must be a non-empty string"`                           |
| `tie_point` coordinates fall outside matrix bounds | `IndexError` | `"tie_point <coords> is out of matrix bounds (<rows>x<cols>)"` |

---

### `report(matrix, seq_a, seq_b, match, mismatch, gap, output_path, tie_point)`

| Condition                                                      | Exception      | Message                                                                                                |
| -------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------ |
| `matrix` is not a 2D NumPy array                               | `TypeError`    | `"matrix must be a 2D numpy array"`                                                                    |
| `seq_a` is empty or not a string                               | `ValueError`   | `"seq_a must be a non-empty string"`                                                                   |
| `seq_b` is empty or not a string                               | `ValueError`   | `"seq_b must be a non-empty string"`                                                                   |
| `matrix.shape` does not match `(len(seq_b)+1, len(seq_a)+1)`   | `ValueError`   | `"matrix shape <actual> does not match expected <expected> for seq_a length <n> and seq_b length <m>"` |
| `tie_point` coordinates fall outside matrix bounds             | `IndexError`   | `"tie_point <coords> is out of matrix bounds (<rows>x<cols>)"`                                         |
| User-provided `output_path` parent directory cannot be created | `OSError`      | `"Cannot create output directory '<path>': <original error>"`                                          |
| Writing figures to PDF fails (disk full, permissions, etc.)    | `RuntimeError` | `"Failed to write PDF report to '<path>': <original error>"`                                           |

**Figure cleanup guarantee:**
All Matplotlib figures (`fig`, `fig2`, `fig3`) are initialized to `None` before any plot is created. A `try/finally` block ensures `plt.close()` is called on every open figure regardless of whether the PDF write succeeded or failed, preventing memory leaks.

---

## `main.py`

### `CreateAlignment.main()`

No internal try/except — exceptions propagate to the top-level guard below.

**Notes:**

- Scoring parameters are read directly from `argparse` (`args.match`, `args.mismatch`, `args.gapscore`), not from interactive prompts. `get_scoring_parameters()` is only reached if those values are `None` (i.e., not possible under normal CLI usage).
- The `__Reports` directory is created with `Path.mkdir(exist_ok=True)` — no error handling needed here as `exist_ok=True` suppresses the already-exists case.

### Top-level guard (`__main__`)

| Condition                                                                            | Behaviour                                                     |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `ValueError`, `TypeError`, `AttributeError`, `IndexError`, `OSError`, `RuntimeError` | Prints `Error: <message>` and exits with code `1`             |
| Any other unexpected exception                                                       | Prints `Unexpected error: <message>` and exits with code `1`  |
| Either outcome (success or failure)                                                  | `__pycache__` directories are always cleaned up via `finally` |

---

## Error Propagation Chain

```
main.py  (top-level try/except → clean exit message)
  └── input_sequences(args)
        ├── validate_fasta_extension()     ← returns False on bad extension (re-prompt)
        ├── validate_fasta_loadable()      ← returns False / sys.exit(1) on bad file
        ├── parse_fasta_file()             ← returns False on FileNotFoundError / empty
        ├── validate_single_fasta_sequence() ← returns False / sys.exit(1) on multi-seq
        ├── validate_fasta_dna()           ← returns False / sys.exit(1) on invalid DNA
        └── build_sequence_input()
              └── validate_dna_sequence()  ← ValueError on invalid chars / empty
  └── parsing(file_from_input, match, mismatch, gap)
        ├── get_scoring_parameters()       ← ValueError on bad int input (fallback only)
        ├── seq extraction                 ← AttributeError on missing .seq_a / .seq_b
        ├── matrix allocation              ← ValueError on bad dimensions
        ├── ASCII encoding                 ← ValueError on non-ASCII sequences
        └── GridBuild.matrix_construct()   ← RuntimeError (wraps any GridBuild error)
  └── report(matrix, seq_a, seq_b, ...)
        ├── Input validation               ← TypeError / ValueError / IndexError
        ├── Output directory creation      ← OSError
        ├── traceback_graphing()           ← TypeError / ValueError / IndexError
        └── PdfPages write                 ← RuntimeError (wraps any I/O failure)
              finally: plt.close() on all figures
```
