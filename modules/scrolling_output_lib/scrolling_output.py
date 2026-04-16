#!/usr/bin/env python3

#escott60@charlotte.edu
#Em Scott

#make a pdf output
import numpy as np #give abbreviation to numpy
import sys
from typing import List, Tuple
from collections import deque
from numba import njit 


class GridBuild():
    @njit
    def matrix_build(self, seq_a: str, seq_b: str, gap: int) -> np.ndarray: #set up the matrix with NumPy
        """
        Purpose: Initialize a matrix with the sequences, getting it ready for output

        Parameters: Take the input cleaned sequences and create a grid based on the size
        
        Returns: Return a tuple containing initialized rows and columns
        """
        rows = len(seq_a) + 1
        cols = len(seq_b) + 1
        matrix = np.zeros((rows, cols), dtype=np.int32)
        matrix[:, 0] = np.arange(rows) * gap
        matrix[0, :] = np.arange(cols) * gap

        #export to main to show the step of the initialization? 
        return matrix

    def matrix_construct(
        self, 
        matrix: np.ndarray,
        seq_a: str, 
        seq_b: str,
        match: int, #get the defaults from CLI, implement getting user-specified parameters later 
        #from parsing.py?
        mismatch: int, 
        gap: int
    ) -> np.ndarray:

        # matrix is already filled by parsing.py — no work needed here
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

        i = matrix.shape[0] - 1
        j = matrix.shape[1] - 1 

        seq_align_a = deque()
        seq_align_b = deque()

        while i > 0 or j > 0:
            if i == 0:
                seq_align_a.appendleft("-")
                seq_align_b.appendleft(seq_b[j-1])
                j -= 1
                continue

            if j == 0:
                seq_align_a.appendleft(seq_a[i-1])
                seq_align_b.appendleft("-")
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
                seq_align_a.appendleft(seq_a[i - 1])
                seq_align_b.appendleft(seq_b[j - 1])
                i -= 1
                j -= 1
            elif current == score_up:
                seq_align_a.appendleft(seq_a[i - 1])
                seq_align_b.appendleft("-")
                i -= 1
            else: # go left:
                seq_align_a.appendleft("-")
                seq_align_b.appendleft(seq_b[j - 1])
                j -= 1

        return seq_align_a, seq_align_b 


    def best_sequence(self, seq_align_a: str, seq_align_b: str) -> List[str]:
        consensus_seq = []
        for a, b in zip(seq_align_a, seq_align_b):
            if a == b:
                consensus_seq.append(a)
            elif a == "-":
                consensus_seq.append(b)
            elif b == "-":
                consensus_seq.append(a)
            else:
                consensus_seq.append("N") #one or the other
        return consensus_seq 

"""
-----------------------------------------------------------------------------------------------------------

TESTING/TROUBLESHOOTING DOCSTRING (When calling on scrolling_output.py)

if __name__ == "__main__":
    call_grid = GridBuild()
    matrix = call_grid.matrix_build("AGATCATCTATCTA", "AGATCATCTGTACATT", -2) #sample
    print(matrix)
    matrix = call_grid.matrix_construct(matrix, "AGATCATCTATCTA", "AGATCATCTGTACATT", 2, -1, -2) #sample
    print(matrix)

    align_a, align_b = call_grid.view_traceback(
        matrix,
        "AGATCATCTATCTA",
        "AGATCATCTGTACATT",
        2, -1, -2
    )

    print("Aligned A:", "".join(align_a))
    print("Aligned B:", "".join(align_b))

    optimal_seq = call_grid.best_sequence(
        "AGATCATCTATCTA",
        "AGATCATCTGTACATT")
    print(optimal_seq)

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