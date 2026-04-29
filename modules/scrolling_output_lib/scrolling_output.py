#!/usr/bin/env python3

#escott60@charlotte.edu
#Em Scott

import sys
import numpy as np
from typing import List, Tuple, Optional 
from collections import deque
from numba import njit 

#IMPORTANT: The first running instance of this program will be slower due to Numba compiling data. 
#After the initial slow run, the speed will be better optimized. 

class GridBuild():
	@njit
	def matrix_build(seq_a: str, seq_b: str, gap: int) -> np.ndarray: #set up the matrix with NumPy
		"""
		Purpose: Initialize a matrix with the sequences by utilizing NumPy, getting it ready for output.
		This function serves as the matrix set up, and creates what can be best described as a scoring
		algorithm with the gap penalty score. 

		Parameters: 
		-Sequence a,
		-Sequence b, 
		-Gap penalty score 
		
		Returns: Returns the NumPy array, consisting of the sequence dimensions. 
		"""
		rows = len(seq_a) + 1
		cols = len(seq_b) + 1
		matrix = np.zeros((rows, cols), dtype=np.int32)

		#The leftmost column is used for initializing all rows
		matrix[:, 0] = np.arange(rows) * gap

		#The top row is reserved for initializing all columns
		matrix[0, :] = np.arange(cols) * gap

		return matrix


	def matrix_construct(
		self, 
		matrix: np.ndarray,
		seq_a: str, 
		seq_b: str,
		match: int, 
		mismatch: int, 
		gap: int
	) -> np.ndarray:
		"""
		Purpose: Simply passes the function to parsing.py for further construction of the matrix. The 
		matrix constructed from the matrix_build() function is passed to def parsing() for match/mismatch 
		calculations.

		Parameters: 
		-Matrix (np.ndarray)
		-Sequence a,
		-Sequence b, 
		-Match Score
		-Mismatch Score
		-Gap penalty score 
		
		Returns: Just returns the matrix from the parsing function in parsing.py
		"""
		return matrix


	def view_traceback(
		self, 
		matrix: np.ndarray,
		seq_a: str, 
		seq_b: str,
		match: int,
		mismatch: int,
		gap: int
	) -> Tuple[List, List]:
		"""
		Purpose: Calculates the optimal alignment path by moving left, upwards, or diagonally
		across the matrix from the bottom right corner.

		Parameters: 
		-Matrix (np.ndarray)
		-Sequence a,
		-Sequence b, 
		-Match Score
		-Mismatch Score
		-Gap penalty score 
		
		Returns: Returns a tuple of two lists. 

		*Note: The two lists are modified with the deque import, but are still considered lists 
		or "list-like objects". 
		"""
		#Start at the bottom right corner of the matrix.
		i = matrix.shape[0] - 1
		j = matrix.shape[1] - 1 

		#Use deque for easy appending/deleting at both ends of lists. Good for calculating alignment
		#scores and traceback. 
		seq_align_a = deque()
		seq_align_b = deque()

		#i for rows
		#j for columns

		#In the case that Sequence A (i) has no more nucleotides remaining
		while i > 0 or j > 0:
			if i == 0:
				seq_align_a.appendleft("-")
				seq_align_b.appendleft(seq_b[j - 1])
				j -= 1
				continue
		#In the case that Sequence B (j) has no more nucleotides remaining
			if j == 0:
				seq_align_a.appendleft(seq_a[i - 1])
				seq_align_b.appendleft("-")
				i -= 1
				continue

			current = matrix[i, j] #remain constant
			diag = matrix[i - 1, j - 1] #move left and up
			up = matrix[i - 1, j] #move up one row
			left = matrix[i, j - 1] #move up one column

			#Matches:
			score_di = diag + (match if seq_b[i - 1] == seq_a[j - 1] else mismatch)

			#Mismatches:
			score_up = up + gap
			score_left = left + gap
		
			if current == score_di: #move diagonally
				seq_align_a.appendleft(seq_a[i - 1])
				seq_align_b.appendleft(seq_b[j - 1])
				i -= 1
				j -= 1
			elif current == score_up: #move up
				seq_align_a.appendleft(seq_a[i - 1])
				seq_align_b.appendleft("-")
				i -= 1
			else: #move left:
				seq_align_a.appendleft("-")
				seq_align_b.appendleft(seq_b[j - 1])
				j -= 1

		# Check for a tie and generate an alt if the tie is found
		tie_point = self.find_ties(matrix, seq_a, seq_b, match, mismatch, gap)
		if tie_point:
			alt_a, alt_b = self.view_traceback(matrix, seq_a, seq_b, match, mismatch, gap, tie_point)
			return (seq_align_a, seq_align_b), (alt_a, alt_b)

		return (seq_align_a, seq_align_b), None 


	def find_ties(
		self,
		matrix: np.ndarray,
		seq_a: str,
		seq_b: str,
		match: int,
		mismatch: int,
		gap: int
	) -> Optional[Tuple]:
		"""
		Purpose: Finds another optimal alignment within the traceback step. May not be 
		present in all sequences. 

		Parameters: 
		-Matrix (np.ndarray)
		-Sequence a,
		-Sequence b, 
		-Match Score
		-Mismatch Score
		-Gap penalty score 
		
		Returns: Returns a tuple of two lists in the case of finding a tie 
		"""

		#Start at the bottom right corner of the matrix.
		i = matrix.shape[0] - 1
		j = matrix.shape[1] - 1 

		#If no more nucleotides remain
		while i > 0 or j > 0:
			if i == 0 or j == 0:
				break
				
			current = matrix[i, j] #remain constant
			diag = matrix[i-1, j-1] #move left and up
			up = matrix[i-1, j] #move up one row
			left = matrix[i, j-1] #move up one column

			#Matches:
			score_di = diag + (match if seq_b[i - 1] == seq_a[j - 1] else mismatch)

			#Mismatches:
			score_up = up + gap
			score_left = left + gap

			#Check how many optimal paths can be found to get to the current cell
			valid = [k for k, v in {"diag": score_di, "up": score_up, "left": score_left}.items() if v == current]

			if len(valid) > 1:
				return (i, j)  #get only the first tie

			if current == score_di: #move diagonally
				i -= 1
				j -= 1
			elif current == score_up: #move up
				i -= 1
			else: #move left:
				j -= 1

		return None


	def tie_traceback(
		self, 
		matrix: np.ndarray,
		seq_a: str, 
		seq_b: str,
		match: int,
		mismatch: int,
		gap: int,
		tie_point: Tuple
	) -> Tuple[List, List]:
		"""
		Purpose: If an alternate optimal alignment is found, performs the traceback step on the alt. alignment,
		following the same logic as view_traceback()

		Parameters: 
		-Matrix (np.ndarray)
		-Sequence a,
		-Sequence b, 
		-Match Score
		-Mismatch Score
		-Gap penalty score 
		-The tie point (where the primary and alt. alignments diverge)
		
		Returns: Returns a tuple of two lists
		"""
		i, j = tie_point
		alt_a = deque()
		alt_b = deque()

		current = matrix[i, j]
		diag = matrix[i-1, j-1]
		up = matrix[i-1, j]
		left = matrix[i, j-1]

		score_di = diag + (match if seq_a[i-1] == seq_b[j-1] else mismatch)
		score_up = up + gap
		score_left = left + gap

		if current == score_di and current == score_up:
			#Tie between diag and up, go up
			alt_a.appendleft(seq_a[i - 1])
			alt_b.appendleft("-")
			i -= 1
		elif current == score_di and current == score_left:
			alt_a.appendleft("-")
			alt_b.appendleft(seq_b[j - 1])
			j -= 1
		else:
			alt_a.appendleft("-")
			alt_b.appendleft(seq_b[j - 1])
			j -= 1

		while i > 0 or j > 0:
			if i == 0:
				alt_a.appendleft("-")
				alt_b.appendleft(seq_b[j-1])
				j -= 1
				continue
			if j == 0:
				alt_a.appendleft(seq_a[i-1])
				alt_b.appendleft("-")
				i -= 1
				continue

			current = matrix[i, j]
			diag = matrix[i-1, j-1]
			up = matrix[i-1, j]
			left = matrix[i, j-1]

			score_di = diag + (match if seq_a[i-1] == seq_b[j-1] else mismatch)
			score_up = up + gap
			score_left = left + gap

			if current == score_di:  
				alt_a.appendleft(seq_a[i - 1])
				alt_b.appendleft(seq_b[j - 1])
				i -= 1
				j -= 1
			elif current == score_up: 
				alt_a.appendleft(seq_a[i - 1])
				alt_b.appendleft("-")
				i -= 1
			else: 
				alt_a.appendleft("-")
				alt_b.appendleft(seq_b[j - 1])
				j -= 1

		return alt_a, alt_b


	def build_consensus(
		self,
		seq_align_a: List,
		seq_align_b: List,
		alt_a: List = None,
		alt_b: List = None
	) -> Tuple[List[str], Optional[List[str]]]:

		"""
		Purpose: Determines the consensus sequence from the alignment. 

		Parameters: 
		-Aligned Sequence A
		-Aligned Sequence B
		-Alternate aligned Sequence A
		-Alternate aligned Sequence B

		Returns: List(s) containing the optimal sequence(s)
		"""

		def best_sequence(self, seq_align_a: str, seq_align_b: str) -> List[str]:
			"""
			Purpose: Determines the consensus sequence from the alignment. 

			Parameters: 
			-Aligned Sequence A
			-Aligned Sequence B

			Returns: A list containing the determined consensus sequence. 
			"""
			consensus_seq = []
			for a, b in zip(seq_align_a, seq_align_b):
			#Doesn't matter here whether the NT from Sequence A or B is appended since it's a match.
				if a == b:
					consensus_seq.append(a)
			#If Sequence A's NT is a gap, append the NT from Sequence B:
				elif a == "-":
					consensus_seq.append(b)
			#If Sequence B's NT is a gap, append the NT from Sequence A:
				elif b == "-":
					consensus_seq.append(a)
			#If both have a nucleotide and disagree:
				else:
					consensus_seq.append("N")
			return consensus_seq 

		first = build_consensus(seq_align_a, seq_align_b)
		alt = build_consensus(alt_a, alt_b) if alt_a and alt_b else None

		return first, alt


"""
-----------------------------------------------------------------------------------------------------------

TESTING/TROUBLESHOOTING DOCSTRING (When calling on scrolling_output.py)

if __name__ == "__main__":
	call_grid = GridBuild()
	matrix = call_grid.matrix_build("AGATCATCTATCTA", "AGATCATCTGTACATT", -2) #sample
	sys.stdout.write(str(matrix) + "\n")
	matrix = call_grid.matrix_construct(matrix, "AGATCATCTATCTA", "AGATCATCTGTACATT", 2, -1, -2) #sample
	sys.stdout.write(str(matrix) + "\n")

	align_a, align_b = call_grid.view_traceback(
		matrix,
		"AGATCATCTATCTA",
		"AGATCATCTGTACATT",
		2, -1, -2
	)

	sys.stdout.write("Aligned A: " + "".join(align_a) + "\n")
	sys.stdout.write("Aligned B: " + "".join(align_b) + "\n")

	optimal_seq = call_grid.best_sequence(
		"AGATCATCTATCTA",
		"AGATCATCTGTACATT")
	sys.stdout.write(str(optimal_seq) + "\n")

-----------------------------------------------------------------------------------------------------------

"""
"""
-----------------------------------------------------------------------------------------------------------

PSEUDOCODE DOCSTRING

Consider putting everything into a class?
Make sure to get all the input parameters
Parameters should include (self):
	sequence 1
	sequence 2
	match score
	mismatch score
	gap penalties
Take all passed input/output from parsing.py
Initialize the matrix and get it formatted for printing
Functions should include: 
	Matrix initialization 
	Matrix construction
	Matrix annotating/traceback
	Matrix printing(?)

-----------------------------------------------------------------------------------------------------------
Major Changes/Updates Timestamping: 

4/12/2026 Update: Added docstrings to all functions, and made sure this module
is fully integrated into program workflow. Imported numba for optimizing speed.
(*Numba has been listed and detailed as a dependency in the README.md file.)

----------------------------------------------------------------------------------------------------------- 

3/26/2026 Update: The script has been tested and works well. However, it can be
further optimized in terms of memory preallocation and the addition of docstrings.

-----------------------------------------------------------------------------------------------------------

2/19/2026

Scrolling output brainstorming: 

Purpose: Create image and table output for user
Input: Scoring matrix file 
Output: Image (likely .png), and a file (.csv or .tsv) of top three choices 
High-level steps: 
Create image formatting for the raw input data alongside the scoring and optimal traceback paths 
Export the image in a viewable, legible format 
.png, jpeg, .pdf 

-----------------------------------------------------------------------------------------------------------
"""

