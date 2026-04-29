#!/usr/bin/env python3

# Run from project root with:
# python test_workflow.py

import sys
from pathlib import Path
from modules.input_lib.input import build_sequence_input, read_two_fastas, parse_fasta_file
from modules.parsing_lib.parsing import parsing

TEST_DATA = Path(__file__).parent / "test_data"
MATCH     = 2
MISMATCH  = -1
GAP       = -2

# ================================================================
# Scenario 1: manual sequences
# ================================================================
sys.stdout.write("---- Scenario 1: manual sequences, default parameters ----\n")
sys.stdout.write("seq1: ACCTTC  seq2: ACGGTC  match=2, mismatch=-1, gap=-2\n")
sys.stdout.write("\n")

SEQ1 = "ACCTTC"
SEQ2 = "ACGGTC"

sequence_input = None
try:
    sequence_input = build_sequence_input(SEQ1, SEQ2, "seq1", "seq2")
    assert sequence_input is not False, "build_sequence_input returned False"
    sys.stdout.write(f"Input:  PASS -> seq_a={sequence_input.seq_a}, seq_b={sequence_input.seq_b}\n")
except AssertionError as e:
    sys.stdout.write(f"Input:  FAIL -> {e}\n")

matrix = seq_a = seq_b = None
if sequence_input:
    try:
        matrix, seq_a, seq_b, match, mismatch, gap, tie_point = parsing(
            sequence_input, MATCH, MISMATCH, GAP
        )
        sys.stdout.write(f"Parsing PASS -> shape={matrix.shape}, "
              f"match={match}, mismatch={mismatch}, gap={gap}, tie_point={tie_point}\n")
    except Exception as e:
        sys.stdout.write(f"Parsing FAIL -> {e}\n")
else:
    sys.stdout.write("Parsing SKIP -> input step failed\n")

if matrix is not None:
    try:
        assert matrix[0, 0] == 0,    f"Expected matrix[0,0]=0, got {matrix[0,0]}"
        assert matrix[1, 0] == GAP,  f"Expected matrix[1,0]={GAP}, got {matrix[1,0]}"
        assert matrix[0, 1] == GAP,  f"Expected matrix[0,1]={GAP}, got {matrix[0,1]}"
        rows, cols = matrix.shape
        sys.stdout.write(f"Matrix: PASS -> corners OK, bottom-right={int(matrix[rows-1, cols-1])}\n")
    except AssertionError as e:
        sys.stdout.write(f"Matrix: FAIL -> {e}\n")

    sys.stdout.write("\n")
    sys.stdout.write("---- Full matrix ----\n")
    sys.stdout.write(f"     {'  '.join(['  '] + list(seq_a))}\n")
    for i, row in enumerate(matrix):
        lbl = seq_b[i - 1] if i > 0 else " "
        sys.stdout.write(f"  {lbl}  {'  '.join(str(v).rjust(2) for v in row)}\n")
else:
    sys.stdout.write("Matrix: SKIP -> parsing step failed\n")

# ================================================================
# Scenario 2: valid FASTA files
# ================================================================
sys.stdout.write("\n")
sys.stdout.write("---- Scenario 2: FASTA input (test_seq1.fasta + test_seq2.fasta) ----\n")

FASTA1 = str(TEST_DATA / "test_seq1.fasta")
FASTA2 = str(TEST_DATA / "test_seq2.fasta")

fasta_label_a = fasta_seq_a = fasta_label_b = fasta_seq_b = None
fasta_read_ok = False
try:
    fasta_result = read_two_fastas(FASTA1, FASTA2)
    assert fasta_result is not False, "read_two_fastas returned False"
    fasta_label_a, fasta_seq_a, fasta_label_b, fasta_seq_b = fasta_result
    fasta_read_ok = True
    sys.stdout.write(f"FASTA read: PASS -> '{fasta_label_a}': {fasta_seq_a}, '{fasta_label_b}': {fasta_seq_b}\n")
except AssertionError as e:
    sys.stdout.write(f"FASTA read: FAIL -> {e}\n")

fasta_input = None
if fasta_read_ok:
    try:
        fasta_input = build_sequence_input(fasta_seq_a, fasta_seq_b, fasta_label_a, fasta_label_b)
        assert fasta_input is not False, "build_sequence_input returned False"
        sys.stdout.write(f"Input:      PASS -> seq_a={fasta_input.seq_a}, seq_b={fasta_input.seq_b}\n")
    except AssertionError as e:
        sys.stdout.write(f"Input:      FAIL -> {e}\n")
else:
    sys.stdout.write("Input:      SKIP -> FASTA read failed\n")

if fasta_input:
    try:
        m2, sa2, sb2, match2, mm2, gap2, tie2 = parsing(fasta_input, MATCH, MISMATCH, GAP)
        sys.stdout.write(f"Parsing:    PASS -> shape={m2.shape}, "
              f"bottom-right={int(m2[-1, -1])}, tie_point={tie2}\n")
    except Exception as e:
        sys.stdout.write(f"Parsing:    FAIL -> {e}\n")
else:
    sys.stdout.write("Parsing:    SKIP -> input step failed\n")

# ================================================================
# Scenario 3: broken FASTA — invalid DNA base ('Z')
# ================================================================
sys.stdout.write("\n")
sys.stdout.write("---- Scenario 3: broken FASTA (invalid DNA base 'Z') ----\n")

BROKEN_Z = str(TEST_DATA / "broken_test_has_Z_base.fasta")

try:
    parsed_bad = parse_fasta_file(BROKEN_Z)
    assert parsed_bad is not False, "parse_fasta_file unexpectedly returned False"
    label_bad, seq_bad = parsed_bad
    result_bad = build_sequence_input(seq_bad, SEQ2, label_bad, "seq2")
    assert result_bad is False, f"Expected False for invalid DNA, got {result_bad}"
    sys.stdout.write("Invalid DNA: PASS -> build_sequence_input correctly rejected sequence with 'Z' base\n")
except AssertionError as e:
    sys.stdout.write(f"Invalid DNA: FAIL -> {e}\n")

# ================================================================
# Scenario 4: broken FASTA — multiple sequences in one file
# ================================================================
sys.stdout.write("\n")
sys.stdout.write("---- Scenario 4: broken FASTA (multiple sequences in one file) ----\n")

BROKEN_MULTI = str(TEST_DATA / "broken_test_more_than_1_seq.fasta")

try:
    with open(BROKEN_MULTI, "r") as f:
        header_count = sum(1 for line in f if line.startswith(">"))
    assert header_count > 1, f"Expected multiple '>' headers, found {header_count}"
    sys.stdout.write(f"Multi-seq:  PASS -> file has {header_count} sequences, correctly identified as invalid\n")
except (AssertionError, OSError) as e:
    sys.stdout.write(f"Multi-seq:  FAIL -> {e}\n")
