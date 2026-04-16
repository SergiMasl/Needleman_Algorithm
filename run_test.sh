#!/usr/bin/env bash
# run_test.sh — automated test for the Needleman-Wunsch alignment tool
# Run from the project root:   bash run_test.sh
#
# Requires the conda environment "needleman_algorithm" (Python 3.11).
# Create it with:  conda env create -f environment.yml
# Then run:        bash run_test.sh

set -uo pipefail

CONDA_ENV="needleman_algorithm"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="conda run --no-capture-output -n $CONDA_ENV python"
PASS=0
FAIL=0

echo "============================================================"
echo "  Needleman-Wunsch Alignment Tool — Test Suite"
echo "============================================================"
echo ""

# ── Test 1: Python module workflow (no PDF, no user prompts) ─────────────────
echo "[Test 1] Inline workflow (ACCTTC vs ACGGTC, defaults)"
OUTPUT=$($PYTHON -m modules.test_workflow 2>&1)

if echo "$OUTPUT" | grep -q "Input:  PASS" && \
   echo "$OUTPUT" | grep -q "Parsing PASS" && \
   echo "$OUTPUT" | grep -q "Matrix: PASS"; then
    echo "  PASS — all three checks passed"
    PASS=$((PASS + 1))
else
    echo "  FAIL — one or more checks failed"
    echo "$OUTPUT"
    FAIL=$((FAIL + 1))
fi
echo ""

# ── Test 2: Bottom-right score check ────────────────────────────────────────
echo "[Test 2] Expected alignment score (ACCTTC vs ACGGTC = 6)"
SCORE=$(echo "$OUTPUT" | grep "bottom-right score" | grep -oE '[0-9-]+$')

if [ "$SCORE" = "6" ]; then
    echo "  PASS — score is $SCORE"
    PASS=$((PASS + 1))
else
    echo "  FAIL — expected 6, got '$SCORE'"
    FAIL=$((FAIL + 1))
fi
echo ""

# ── Test 3: FASTA file parsing ───────────────────────────────────────────────
echo "[Test 3] FASTA file parse (test_data/test_seq1.fasta)"
FASTA_OUT=$($PYTHON -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR')
from modules.input_lib.input import parse_fasta_file
result = parse_fasta_file('$SCRIPT_DIR/test_data/test_seq1.fasta')
print('OK' if result and result[1] == 'ACCTTC' else 'FAIL: ' + str(result))
" 2>&1)

if [ "$FASTA_OUT" = "OK" ]; then
    echo "  PASS"
    PASS=$((PASS + 1))
else
    echo "  FAIL — $FASTA_OUT"
    FAIL=$((FAIL + 1))
fi
echo ""

# ── Test 4: DNA validation rejects bad input ─────────────────────────────────
echo "[Test 4] Validation rejects invalid DNA characters"
VAL_OUT=$($PYTHON -c "
import sys; sys.path.insert(0, '$SCRIPT_DIR')
from modules.validation_lib.validation import validate_dna_sequence
try:
    validate_dna_sequence('ACXGT', name='test')
    print('FAIL: no exception raised')
except ValueError:
    print('OK')
" 2>&1)

if [ "$VAL_OUT" = "OK" ]; then
    echo "  PASS"
    PASS=$((PASS + 1))
else
    echo "  FAIL — $VAL_OUT"
    FAIL=$((FAIL + 1))
fi
echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
echo "============================================================"
echo "  Results: $PASS passed, $FAIL failed"
echo "============================================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
