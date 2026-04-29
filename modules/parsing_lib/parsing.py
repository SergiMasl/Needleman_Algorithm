#!/usr/bin/env python3

from typing import Optional, Tuple
import numpy as np
from modules.parsing_lib.get_scoring_parameters import get_scoring_parameters
from modules.scrolling_output_lib.scrolling_output import GridBuild

def parsing(
    file_from_input,
    match_score: Optional[int] = None,
    mismatch_score: Optional[int] = None,
    gap_penalty: Optional[int] = None,
) -> Tuple[np.ndarray, str, str, int, int, int, Optional[Tuple[int, int]]]:
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
	try:
		seq_a = file_from_input.seq_a  # columns
		seq_b = file_from_input.seq_b  # rows
	except AttributeError as e:
		raise AttributeError(f"Input object is missing sequence data: {e}")

	rows = len(seq_b) + 1
	cols = len(seq_a) + 1

	try:
		matrix = np.zeros((rows, cols), dtype=int)
	except ValueError as e:
		raise ValueError(f"Could not allocate scoring matrix ({rows}x{cols}): {e}")

	# lambdas for the three scoring operations used in the NW recurrence
	gap_score  = lambda val: val + gap_penalty
	char_score = np.vectorize(lambda b, a: match_score if b == a else mismatch_score)
	cell_score = lambda d, u, l: max(d, u, l)

	# initialize borders: each border cell = its index * gap_penalty
	gap_init       = lambda n: np.arange(1, n) * gap_penalty
	matrix[1:, 0]  = gap_init(rows)
	matrix[0, 1:]  = gap_init(cols)

	# precompute match/mismatch scores for every (i,j) pair at once
	try:
		seq_b_arr = np.frombuffer(seq_b.encode(), dtype=np.uint8)
		seq_a_arr = np.frombuffer(seq_a.encode(), dtype=np.uint8)
	except (UnicodeEncodeError, AttributeError) as e:
		raise ValueError(f"Sequences must be ASCII strings: {e}")

	diag_scores = char_score(seq_b_arr[:, None], seq_a_arr[None, :])

	# fill matrix — single pass, no character comparison inside the loop
	for i in range(1, rows):
		for j in range(1, cols):
			diagonal    = matrix[i - 1, j - 1] + diag_scores[i - 1, j - 1]
			up          = gap_score(matrix[i - 1, j])
			left        = gap_score(matrix[i, j - 1])
			matrix[i, j] = cell_score(diagonal, up, left)

	try:
		grid = GridBuild()
		grid.matrix_construct(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty)
	except Exception as e:
		raise RuntimeError(f"Failed to construct display grid: {e}")
	# Run the tie alignment if applicable:
	tie_point = grid.find_ties(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty)

	return matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty, tie_point


#Sergey will be doing the parsing function(s)