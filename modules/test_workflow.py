# Run from project root with:
# python -m modules.test_workflow

from modules.input_lib.input import build_sequence_input
from modules.parsing_lib.parsing import parsing

print("---- Workflow test: manual sequences, default parameters ----")
print("seq1: ACCTTC")
print("seq2: ACGGTC")
print("match=2, mismatch=-1, gap=-2")
print()

# Scenario 1: manual sequences with default scoring parameters
SEQ1 = "ACCTTC"
SEQ2 = "ACGGTC"
MATCH = 2
MISMATCH = -1
GAP = -2

# Step 1: build and validate sequence input
try:
    sequence_input = build_sequence_input(SEQ1, SEQ2, "seq1", "seq2")
    assert sequence_input is not False, "build_sequence_input returned False"
    print(f"Input:  PASS -> seq_a={sequence_input.seq_a}, seq_b={sequence_input.seq_b}")
except AssertionError as e:
    print(f"Input:  FAIL -> {e}")

# Step 2: run parsing (NW matrix construction)
try:
    matrix, seq_a, seq_b, match, mismatch, gap = parsing(
        sequence_input, MATCH, MISMATCH, GAP
    )
    print(f"Parsing PASS -> matrix shape={matrix.shape}, "
          f"match={match}, mismatch={mismatch}, gap={gap}")
except Exception as e:
    print(f"Parsing FAIL -> {e}")

# Step 3: spot-check matrix corners and bottom-right score
try:
    assert matrix[0, 0] == 0,           f"Expected matrix[0,0]=0, got {matrix[0,0]}"
    assert matrix[1, 0] == GAP,         f"Expected matrix[1,0]={GAP}, got {matrix[1,0]}"
    assert matrix[0, 1] == GAP,         f"Expected matrix[0,1]={GAP}, got {matrix[0,1]}"

    rows, cols = matrix.shape
    bottom_right = int(matrix[rows - 1, cols - 1])
    print(f"Matrix: PASS -> corners OK, bottom-right score={bottom_right}")
except AssertionError as e:
    print(f"Matrix: FAIL -> {e}")

print()
print("---- Full matrix ----")
print(f"     {'  '.join(['  '] + list(seq_a))}")
for i, row in enumerate(matrix):
    label = seq_b[i - 1] if i > 0 else " "
    print(f"  {label}  {'  '.join(str(v).rjust(2) for v in row)}")
