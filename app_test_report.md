# Application Test Report

**Project:** Needleman-Wunsch Global Alignment Tool  
**Date:** 2026-04-29

---

## 1. Overview

The application performs pairwise DNA sequence alignment using the Needleman-Wunsch algorithm. It accepts sequences either as inline strings or from FASTA files, validates input, fills the scoring matrix, runs a traceback (including tie detection), and outputs a multi-page PDF report.

Modules under test:

| Module                      | File                                               |
| --------------------------- | -------------------------------------------------- |
| Input handling              | `modules/input_lib/input.py`                       |
| Sequence validation         | `modules/validation_lib/validation.py`             |
| Scoring matrix construction | `modules/parsing_lib/parsing.py`                   |
| Traceback & tie detection   | `modules/scrolling_output_lib/scrolling_output.py` |
| PDF report generation       | `modules/report_lib/report.py`                     |
| CLI entry point             | `main.py`                                          |

---

## 2. Test Results Summary

| Suite                                        | Tests  | Passed | Failed |
| -------------------------------------------- | ------ | ------ | ------ |
| Integration workflow (`test_workflow.py`)    | 8      | 8      | 0      |
| Validation unit tests (`test_validation.py`) | 11     | 11     | 0      |
| **Total**                                    | **19** | **19** | **0**  |

---

## 3. Integration Workflow Tests (`test_workflow.py`)

Run command: `python test_workflow.py`

### Scenario 1 — Manual sequences, default scoring parameters

**Input:** `seq1 = ACCTTC`, `seq2 = ACGGTC`, match=2, mismatch=−1, gap=−2

| Step                   | Result | Detail                                                              |
| ---------------------- | ------ | ------------------------------------------------------------------- |
| `build_sequence_input` | PASS   | `seq_a=ACCTTC`, `seq_b=ACGGTC`                                      |
| `parsing`              | PASS   | matrix shape=(7,7), match=2, mismatch=−1, gap=−2, tie_point=None    |
| Matrix corner check    | PASS   | `matrix[0,0]=0`, `matrix[1,0]=−2`, `matrix[0,1]=−2`, bottom-right=6 |

Full scoring matrix produced:

```
         A   C   C   T   T   C
     [  0  -2  -4  -6  -8 -10 -12 ]
  A  [ -2   2   0  -2  -4  -6  -8 ]
  C  [ -4   0   4   2   0  -2  -4 ]
  G  [ -6  -2   2   3   1  -1  -3 ]
  G  [ -8  -4   0   1   2   0  -2 ]
  T  [-10  -6  -2  -1   3   4   2 ]
  C  [-12  -8  -4   0   1   2   6 ]
```

Optimal alignment score: **6**

---

### Scenario 2 — FASTA file input

**Input files:** `test_data/test_seq1.fasta` (ACCCTC), `test_data/test_seq2.fasta` (ACGGTC)

| Step                   | Result | Detail                                                |
| ---------------------- | ------ | ----------------------------------------------------- |
| `read_two_fastas`      | PASS   | labels and sequences correctly parsed from both files |
| `build_sequence_input` | PASS   | `seq_a=ACCCTC`, `seq_b=ACGGTC`                        |
| `parsing`              | PASS   | shape=(7,7), bottom-right=6, tie_point=None           |

---

### Scenario 3 — Invalid DNA base (`Z`) in FASTA

**Input file:** `test_data/broken_test_has_Z_base.fasta` — contains sequence `aaaccactZ`

| Step                   | Result | Detail                                                            |
| ---------------------- | ------ | ----------------------------------------------------------------- |
| `parse_fasta_file`     | PASS   | file parsed, raw sequence returned                                |
| `build_sequence_input` | PASS   | correctly returned `False`; validation rejected the `Z` character |

Validation error message fired:  
`[Error] se3| Test sequence 1 (6 bp) contains invalid character(s): Z. Only A, C, G, and T are allowed.`

---

### Scenario 4 — Multiple sequences in one FASTA file

**Input file:** `test_data/broken_test_more_than_1_seq.fasta` — contains 2 `>` headers

| Step               | Result | Detail                                                     |
| ------------------ | ------ | ---------------------------------------------------------- |
| Header count check | PASS   | 2 sequences detected; file correctly identified as invalid |

---

## 4. Validation Unit Tests (`modules/validation_lib/test_validation.py`)

Run command: `python -m modules.validation_lib.test_validation`

### DNA Sequence Validation (`validate_dna_sequence`)

| Input       | Name      | Expected        | Result | Detail                               |
| ----------- | --------- | --------------- | ------ | ------------------------------------ |
| `"ACGT"`    | seq1      | PASS            | PASS   | Returned `ACGT`                      |
| `"acgt"`    | seq2      | PASS            | PASS   | Normalized to `ACGT`                 |
| `"A C G T"` | seq3      | PASS            | PASS   | Whitespace stripped, returned `ACGT` |
| `"ACGTX"`   | bad_seq   | FAIL (expected) | PASS   | Rejected: invalid character `X`      |
| `""`        | empty_seq | FAIL (expected) | PASS   | Rejected: empty sequence             |
| `None`      | none_seq  | FAIL (expected) | PASS   | Rejected: treated as empty           |

### Integer Validation (`validate_int`)

| Input   | Name       | Expected        | Result | Detail                   |
| ------- | ---------- | --------------- | ------ | ------------------------ |
| `2`     | match      | PASS            | PASS   | Returned `2`             |
| `"-1"`  | mismatch   | PASS            | PASS   | String parsed to `-1`    |
| `"-2"`  | gap        | PASS            | PASS   | String parsed to `-2`    |
| `"abc"` | bad_value  | FAIL (expected) | PASS   | Rejected: not an integer |
| `None`  | none_value | FAIL (expected) | PASS   | Rejected: not an integer |

---

## 5. Module-Level Observations

### Input (`input.py`)

- `parse_fasta_file` correctly reads the first sequence only and stops at a second `>` header.
- `read_two_fastas` returns `False` when either file fails rather than propagating a crash.
- `build_sequence_input` delegates validation to `validation.py` and returns `False` (not an exception) on bad input, giving callers a clean way to handle errors.

### Validation (`validation.py`)

- `normalize_sequence` handles `None`, mixed-case, and whitespace-padded input uniformly.
- `validate_dna_sequence` raises `ValueError` with a descriptive message listing the specific invalid characters.
- `validate_int` correctly rejects non-numeric strings and `None`.
- `validate_fasta_extension`, `validate_fasta_loadable`, and `validate_single_fasta_sequence` guard file input before parsing occurs; they prompt the user to retry or exit rather than crashing.

### Parsing (`parsing.py`)

- Border initialization uses vectorized `np.arange` rather than a Python loop.
- The diagonal score lookup (`diag_scores`) is precomputed for the entire matrix before the fill loop — avoids repeated character comparisons inside the inner loop.
- Tie detection is called via `GridBuild.find_ties` at the end of every parse; result is passed through to the report.

### Scrolling Output (`scrolling_output.py`)

- `find_ties` traverses the standard traceback path and returns the first cell where two or more moves are equally optimal.
- `tie_traceback` takes that cell and re-traces an alternate path from it to the origin.
- `build_consensus` produces an `N` for positions where both aligned nucleotides differ (not a gap).

### Report (`report.py`)

- Validates matrix shape against sequence lengths before drawing.
- Highlights the traceback path in light grey with bold text.
- When a tie is present, generates a third page with the alternate traceback highlighted.
- A `try/finally` block guarantees all matplotlib figures are closed even if PDF writing fails.
