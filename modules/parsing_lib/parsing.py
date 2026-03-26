import numpy as np
from modules.parsing_lib.get_scoring_parameters import get_scoring_parameters
from modules.scrolling_output_lib.scrolling_output import GridBuild

def parsing(file_from_input, match_score=None, mismatch_score=None, gap_penalty=None):
    """
     -this function will take one array which contain 2 seqs arrays
     - step 1: ask user asking user for match score, mismatch score, and gap penalty
     - step 2: put the two DNA sequences in a table-like array, and calculate the scoring values for the matrix, and score the values properly and be able to tabulate properly,

        Purpose: Puts the two DNA sequences in a table-like array
        Input: Taking the two DNA sequences from the User Input File output
        Output: Scoring values for the matrix and rank top three choices

        High-level steps:
        -    Calculate the scoring values for the matrix
        -    Score the values properly and be able to tabulate properly
        -    No data table mismatch or shifts
        -    Be able to compensate if the sequence lengths are not the same
        -    Be capable of performing a traceback (multiple tracebacks if required) to find the most aligned sequences
        -    Be able to rank the top three choices(?), and have tie-rank capabilities

        PSEUDOCODE:
        -----------------------------------------------------------
        FUNCTION parsing(file_from_input):

            # STEP 1 — get scoring parameters
            ask user: use defaults or enter match, mismatch, gap values?
            set match_score, mismatch_score, gap_penalty

            # STEP 2 — extract sequences
            seq_a = file_from_input.seq_a   (goes across columns)
            seq_b = file_from_input.seq_b   (goes down rows)

            # STEP 3 — create empty matrix of size (len(seq_b)+1) x (len(seq_a)+1)
            fill entire matrix with 0s

            # STEP 4 — initialize borders with cumulative gap penalties
            for each row i from 1 to len(seq_b):
                matrix[i][0] = i * gap_penalty
            for each col j from 1 to len(seq_a):
                matrix[0][j] = j * gap_penalty

            # STEP 5 — fill matrix cell by cell (NW recurrence)
            for each row i from 1 to len(seq_b):
                for each col j from 1 to len(seq_a):
                    if seq_b[i-1] == seq_a[j-1]:
                        diagonal = matrix[i-1][j-1] + match_score
                    else:
                        diagonal = matrix[i-1][j-1] + mismatch_score
                    up   = matrix[i-1][j] + gap_penalty
                    left = matrix[i][j-1] + gap_penalty
                    matrix[i][j] = max(diagonal, up, left)

            # STEP 6 — return results for scrolling_output to display
            return matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty
        -----------------------------------------------------------
    """

    # step 1: use provided scoring params, or ask user if not supplied
    if match_score is None or mismatch_score is None or gap_penalty is None:
        match_score, mismatch_score, gap_penalty = get_scoring_parameters()

    # step 2: build the Needleman-Wunsch scoring matrix
    seq_a = file_from_input.seq_a  # columns
    seq_b = file_from_input.seq_b  # rows

    rows = len(seq_b) + 1
    cols = len(seq_a) + 1

    matrix = np.zeros((rows, cols), dtype=int)

    # initialize first column and first row with cumulative gap penalties
    for i in range(1, rows):
        matrix[i][0] = i * gap_penalty
    for j in range(1, cols):
        matrix[0][j] = j * gap_penalty

    # fill the rest of the matrix using NW recurrence
    for i in range(1, rows):
        for j in range(1, cols):
            if seq_b[i - 1] == seq_a[j - 1]:
                diagonal = matrix[i - 1][j - 1] + match_score
            else:
                diagonal = matrix[i - 1][j - 1] + mismatch_score
            up   = matrix[i - 1][j] + gap_penalty
            left = matrix[i][j - 1] + gap_penalty
            matrix[i][j] = max(diagonal, up, left)

    grid = GridBuild()
    grid.matrix_construct(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty)

    return matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty



#Sergey will be doing the parsing function(s)