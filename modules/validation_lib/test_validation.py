"""
test_validation.py

Test script for validation.py

Purpose:
- Test DNA sequence validation with valid and invalid inputs
- Test integer validation with valid and invalid values
- Confirm that error handling works correctly

Run from project root with:
python -m modules.validation_lib.test_validation
"""

# Updated by: Mehrnoush Fereydouni
# Last Updated: April, 23 2026
# Changes:
# - Added test cases for DNA sequence validation
# - Added test cases for integer validation
# - Added PASS / FAIL output formatting
# - Included valid and invalid input examples


import sys
from modules.validation_lib.validation import validate_dna_sequence, validate_int


sys.stdout.write("---- DNA Sequence Tests ----\n")

# Test DNA sequence inputs
test_sequences = [
    ("ACGT", "seq1"),
    ("acgt", "seq2"),
    ("A C G T", "seq3"),
    ("ACGTX", "bad_seq"),
    ("", "empty_seq"),
    (None, "none_seq"),
]

for seq, name in test_sequences:
    try:
        result = validate_dna_sequence(seq, name=name)
        sys.stdout.write(f"{name}: PASS -> {result}\n")
    except ValueError as e:
        sys.stdout.write(f"{name}: FAIL -> {e}\n")


sys.stdout.write("\n---- Integer Tests ----\n")

# Test integer inputs
test_values = [
    (2, "match"),
    ("-1", "mismatch"),
    ("-2", "gap"),
    ("abc", "bad_value"),
    (None, "none_value"),
]

for value, name in test_values:
    try:
        result = validate_int(value, name=name)
        sys.stdout.write(f"{name}: PASS -> {result}\n")
    except ValueError as e:
        sys.stdout.write(f"{name}: FAIL -> {e}\n")
