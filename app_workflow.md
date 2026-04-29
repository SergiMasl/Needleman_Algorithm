# Workflow — Needleman-Wunsch Global Alignment Tool

## Pipeline Overview

```
main.py
  |
  |-- [Step 1] input_lib/input.py          -> collect & validate raw sequences
  |-- [Step 2] parsing_lib/
  |       |-- get_scoring_parameters.py    -> collect scoring values from user
  |       `-- parsing.py                   -> build & fill NW scoring matrix
  |-- [Step 3] scrolling_output_lib/
  |       `-- scrolling_output.py          -> display matrix, traceback, consensus
  `-- [Step 4] report_lib/report.py        -> save PDF report to __Reports/
```

---

## Step-by-Step Description

### Step 1 — Sequence Input (`input_lib/input.py`)

|                 |                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Entry point** | `input_sequences(args)`                                                                                              |
| **Purpose**     | Ask the user how to provide sequences (FASTA file or manual entry), then read, clean, and validate both DNA strings. |
| **Output**      | `SequenceInput` object                                                                                               |

Substeps:

- **1a.** User picks `fasta` or `manual`.
- **1b (fasta).** User enters full path to the first FASTA file, then full path to the second FASTA file. `parse_fasta_file()` opens each file, extracts the first sequence and its label.
- **1b (manual).** User types both DNA sequences directly in the terminal.
- **1c.** `validate_dna_sequence()` (via `volidation_lib`) — strips whitespace, uppercases, rejects anything that is not A / C / G / T.
- **1d.** `build_sequence_input()` — packages both sequences into a `SequenceInput` dataclass (`seq_a`, `seq_b`, `label_a`, `label_b`).

---

### Step 2a — Scoring Parameters (`parsing_lib/get_scoring_parameters.py`)

|                 |                                                                     |
| --------------- | ------------------------------------------------------------------- |
| **Entry point** | `get_scoring_parameters()`                                          |
| **Purpose**     | Ask the user whether to use default scoring or enter custom values. |
| **Defaults**    | match = `+2`, mismatch = `-1`, gap = `-2`                           |
| **Output**      | `(match_score, mismatch_score, gap_penalty)` as integers            |

---

### Step 2b — Matrix Construction (`parsing_lib/parsing.py`)

|                 |                                                                      |
| --------------- | -------------------------------------------------------------------- |
| **Entry point** | `parsing(file_from_input, match_score, mismatch_score, gap_penalty)` |
| **Purpose**     | Build the Needleman-Wunsch scoring matrix from the two sequences.    |
| **Output**      | `(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty)`   |

Substeps:

- **2b-1.** Extract `seq_a` (columns) and `seq_b` (rows) from `SequenceInput`.
- **2b-2.** Allocate a NumPy zero matrix of size `(len(seq_b)+1) x (len(seq_a)+1)`.
- **2b-3.** Initialize borders:
  - first column → `i * gap_penalty`
  - first row → `j * gap_penalty`
- **2b-4.** Fill each cell using the NW recurrence:
  ```
  diagonal = prev_diagonal + (match if chars equal else mismatch)
  up       = cell above    + gap_penalty
  left     = cell to left  + gap_penalty
  cell     = max(diagonal, up, left)
  ```
- **2b-5.** Call `GridBuild.matrix_construct()` to display the matrix in the terminal.

---

### Step 3 — Scrolling Output / Traceback (`scrolling_output_lib/scrolling_output.py`)

|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| **Entry point** | `GridBuild` class methods                                                  |
| **Purpose**     | Visualise the scoring matrix and compute the optimal alignment.            |
| **Output**      | aligned `seq_a`, aligned `seq_b`, consensus sequence (printed to terminal) |

Methods:
| Method | Description |
|---|---|
| `matrix_build()` | Initialise a fresh matrix with gap-border values |
| `matrix_construct()` | Fill the matrix using the NW recurrence |
| `view_traceback()` | Walk back from the bottom-right cell to recover the aligned sequences |
| `best_sequence()` | Merge aligned sequences into a consensus (matches kept, gaps resolved, mismatches → `N`) |

---

### Step 4 — Report Generation (`report_lib/report.py`)

|                 |                                                                        |
| --------------- | ---------------------------------------------------------------------- |
| **Entry point** | `report(matrix, seq_a, seq_b, match, mismatch, gap, output_path=None)` |
| **Purpose**     | Render the scoring matrix as a PDF and save it to `__Reports/`.        |
| **Output**      | PDF file path (also printed to terminal)                               |

Substeps:

- **4a.** `main.py` prompts the user for a report name; default is a datetime-stamped filename: `YYYY-MM-DD_HH-MM-SS.pdf`
- **4b.** Build column/row labels from `seq_a` and `seq_b`.
- **4c.** Render a matplotlib table figure with the matrix values.
- **4d.** Add a title showing match / mismatch / gap parameters.
- **4e.** Save the figure to a `PdfPages` file and close the figure.

---

## Data Flow Diagram

```
User / CLI args
     |
     v
input_sequences(args)
     |  SequenceInput(seq_a, seq_b, label_a, label_b)
     v
get_scoring_parameters()
     |  (match, mismatch, gap)
     v
parsing(file_from_input, match, mismatch, gap)
     |  (matrix, seq_a, seq_b, match, mismatch, gap)
     |       |
     |       `--> GridBuild.matrix_construct()  [terminal display]
     v
[main.py] prompt user for report filename
     |  output_path
     v
report(matrix, seq_a, seq_b, match, mismatch, gap, output_path)
     |
     v
__Reports/<filename>.pdf
```

---

## Module Dependency Map

```
main.py
├── modules/input_lib/input.py
│   └── modules/volidation_lib/validation.py
├── modules/parsing_lib/get_scoring_parameters.py
├── modules/parsing_lib/parsing.py
│   ├── modules/parsing_lib/get_scoring_parameters.py
│   └── modules/scrolling_output_lib/scrolling_output.py
└── modules/report_lib/report.py
```

---

## Key Data Structures

### `SequenceInput` (dataclass)

| Field      | Type  | Description                                     |
| ---------- | ----- | ----------------------------------------------- |
| `.seq_a`   | `str` | First DNA sequence — goes across matrix columns |
| `.seq_b`   | `str` | Second DNA sequence — goes down matrix rows     |
| `.label_a` | `str` | Name/label of `seq_a`                           |
| `.label_b` | `str` | Name/label of `seq_b`                           |

### `matrix` (`np.ndarray[int]`)

| Cell     | Value                              |
| -------- | ---------------------------------- |
| Shape    | `(len(seq_b) + 1, len(seq_a) + 1)` |
| `[0, 0]` | `0` (origin)                       |
| `[i, 0]` | `i * gap_penalty` (left border)    |
| `[0, j]` | `j * gap_penalty` (top border)     |
| `[i, j]` | NW recurrence value                |
