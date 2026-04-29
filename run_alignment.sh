#!/usr/bin/env bash
# =============================================================================
# Alyssa Leite aleite@charlotte.edu
# run_alignment.sh
# Runs the Needleman-Wunsch global alignment tool on two DNA sequences.
#
# Usage (locally):   bash run_alignment.sh
# Usage (on HPC):    sbatch run_alignment.sh
# =============================================================================

# --- SLURM job settings ------------------------------------------------------
# Ignored when running locally — only apply when submitted via 'sbatch'
#SBATCH --job-name=needleman_align
#SBATCH --output=logs/align_%j.out
#SBATCH --error=logs/align_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1

set -euo pipefail

# --- Environment -------------------------------------------------------------
CONDA_ENV="needleman_algorithm"

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"
echo "Conda environment activated: $CONDA_ENV"

# --- Paths -------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN="$SCRIPT_DIR/main.py"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# =============================================================================
# INPUT — edit your sequences and FASTA paths here
# =============================================================================

# --- Manual inline sequences -------------------------------------------------
SEQ_A="AGATCATCTA"       # first DNA sequence  (A/C/G/T only)
SEQ_B="AGATCATCTG"       # second DNA sequence (A/C/G/T only)

# --- FASTA files -------------------------------------------------------------
FASTA_A="$SCRIPT_DIR/test_data/test_seq1.fasta"   # path to first FASTA file
FASTA_B="$SCRIPT_DIR/test_data/test_seq2.fasta"   # path to second FASTA file

# =============================================================================
# Scoring parameters
# =============================================================================
MATCH=2         # score added when two bases match
MISMATCH=-1     # penalty when two bases do not match
GAP=-2          # penalty when a gap is introduced

# =============================================================================
# Output
# =============================================================================
OUTPUT_PDF="alignment_result.pdf"   # saved automatically to __Reports/ by main.py

# =============================================================================
# Ask user which input mode to use
# =============================================================================
echo ""
echo "How would you like to input sequences?"
echo "  1) Manual inline sequences"
echo "  2) FASTA files"
read -p "Enter 1 or 2: " INPUT_CHOICE
echo ""

if [ "$INPUT_CHOICE" = "1" ]; then
    INPUT_MODE="manual"
elif [ "$INPUT_CHOICE" = "2" ]; then
    INPUT_MODE="fasta"
else
    echo "[ERROR] Invalid choice. Please enter 1 or 2."
    exit 1
fi

# =============================================================================
# Run
# =============================================================================
echo "Starting alignment..."
echo "Mode     : $INPUT_MODE"
echo "Match    : $MATCH  |  Mismatch: $MISMATCH  |  Gap: $GAP"
echo "Output   : __Reports/$OUTPUT_PDF"
echo ""

if [ "$INPUT_MODE" = "manual" ]; then
    echo "Seq A : $SEQ_A"
    echo "Seq B : $SEQ_B"
    echo ""

    # printf pipes answers to interactive prompts automatically:
    #   line 1: "manual" -> answers fasta/manual prompt
    #   line 2: $SEQ_A   -> answers "Enter first DNA sequence:"
    #   line 3: $SEQ_B   -> answers "Enter second DNA sequence:"
    printf "manual\n%s\n%s\n" "$SEQ_A" "$SEQ_B" | python "$MAIN" \
        --match "$MATCH" \
        --mismatch "$MISMATCH" \
        --gapscore "$GAP" \
        --outputpdf "$OUTPUT_PDF"

elif [ "$INPUT_MODE" = "fasta" ]; then
    echo "FASTA A : $FASTA_A"
    echo "FASTA B : $FASTA_B"
    echo ""

    # printf pipes answers to interactive prompts automatically:
    #   line 1: "fasta"   -> answers fasta/manual prompt
    #   line 2: $FASTA_A  -> answers "Enter full path to first FASTA file:"
    #   line 3: $FASTA_B  -> answers "Enter full path to second FASTA file:"
    printf "fasta\n%s\n%s\n" "$FASTA_A" "$FASTA_B" | python "$MAIN" \
        --match "$MATCH" \
        --mismatch "$MISMATCH" \
        --gapscore "$GAP" \
        --outputpdf "$OUTPUT_PDF"
fi

echo ""
echo "Alignment complete."
echo "Report saved to: $SCRIPT_DIR/__Reports/$OUTPUT_PDF"