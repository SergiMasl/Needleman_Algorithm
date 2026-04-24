# Alyssa Leite aleite@charlotte.edu
# run_alignment.sh
# Runs the Needleman-Wunsch global alignment tool on two DNA sequences.
#
# Usage (locally):   bash run_alignment.sh
# Usage (on HPC):    sbatch run_alignment.sh
#
# To use FASTA files instead of inline sequences, see the INPUT section below.
# =============================================================================

set -euo pipefail
 
# --- Environment -------------------------------------------------------------
CONDA_ENV="needleman_algorithm"
 
# source conda so 'conda activate' is available in this shell session
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"
echo "[INFO] Conda environment activated: $CONDA_ENV"
 
# --- Paths -------------------------------------------------------------------
# resolve the directory this script lives in, regardless of where you call it from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN="$SCRIPT_DIR/main.py"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"   # create logs/ folder if it doesn't already exist
 
# --- Inputs ------------------------------------------------------------------
# Option A: inline sequences (uncomment these two lines and comment out Option B)
INPUT_MODE="manual"
SEQ_A="AGATCATCTA"    # first DNA sequence  (A/C/G/T only)
SEQ_B="AGATCATCTG"    # second DNA sequence (A/C/G/T only)
 
# Option B: FASTA files (uncomment these and set INPUT_MODE="fasta" above)
# INPUT_MODE="fasta"
# FASTA_A="$SCRIPT_DIR/test_data/seq1.fasta"   # path to first FASTA file
# FASTA_B="$SCRIPT_DIR/test_data/seq2.fasta"   # path to second FASTA file
 
# --- Scoring parameters ------------------------------------------------------
MATCH=2         # score added when two bases match
MISMATCH=-1     # penalty when two bases don't match
GAP=-2          # penalty for inserting a gap
 
# --- Output ------------------------------------------------------------------
OUTPUT_PDF="alignment_result.pdf"   # filename for the PDF report
                                     # saved automatically to __Reports/ by main.py
 
# =============================================================================
# Run
# =============================================================================
echo "[INFO] Starting alignment..."
echo "[INFO] Mode     : $INPUT_MODE"
echo "[INFO] Match    : $MATCH  |  Mismatch: $MISMATCH  |  Gap: $GAP"
echo "[INFO] Output   : __Reports/$OUTPUT_PDF"
echo ""
 
if [ "$INPUT_MODE" = "manual" ]; then
    echo "[INFO] Seq A : $SEQ_A"
    echo "[INFO] Seq B : $SEQ_B"
    echo ""
 
    # pipe the answers to interactive prompts directly into main.py:
    #   line 1: "manual"  -> answers the fasta/manual question
    #   line 2: $SEQ_A    -> answers "Enter first DNA sequence:"
    #   line 3: $SEQ_B    -> answers "Enter second DNA sequence:"
    printf "manual\n%s\n%s\n" "$SEQ_A" "$SEQ_B" | python "$MAIN" \
        --match "$MATCH" \
        --mismatch "$MISMATCH" \
        --gapscore "$GAP" \
        --outputpdf "$OUTPUT_PDF"
 
elif [ "$INPUT_MODE" = "fasta" ]; then
    echo "[INFO] FASTA A : $FASTA_A"
    echo "[INFO] FASTA B : $FASTA_B"
    echo ""
 
    # pipe the answers to interactive prompts for FASTA mode:
    #   line 1: "fasta"    -> answers the fasta/manual question
    #   line 2: $FASTA_A   -> answers "Enter full path to first FASTA file:"
    #   line 3: $FASTA_B   -> answers "Enter full path to second FASTA file:"
    printf "fasta\n%s\n%s\n" "$FASTA_A" "$FASTA_B" | python "$MAIN" \
        --match "$MATCH" \
        --mismatch "$MISMATCH" \
        --gapscore "$GAP" \
        --outputpdf "$OUTPUT_PDF"
 
else
    echo "[ERROR] INPUT_MODE must be 'manual' or 'fasta'. Got: $INPUT_MODE"
    exit 1
fi
 
echo ""
echo "[INFO] Alignment complete."
echo "[INFO] Report saved to: $SCRIPT_DIR/__Reports/$OUTPUT_PDF"