#!/usr/bin/env python3

#escott60@charlotte.edu
#Em Scott

#make a pdf output
import numpy as np #give abbreviation to numpy
import sys
from typing import List, Tuple

"""
3/26/2026 Update: The script has been tested and works well. However, it can be
further optimized in terms of memory preallocation and the addition of docstrings.
"""
#from parsing_lib.parsing import (the parsing return)

class GridBuild():

    def matrix_build(self, seq_a: str, seq_b: str, gap: int) -> np.ndarray: #set up the matrix with NumPy
        """
        Purpose: Initialize a matrix with the sequences, getting it ready for output

        Parameters: Take the input cleaned sequences and create a grid based on the size
        
        Returns: Return a tuple containing initialized rows and columns
        """
        rows = len(seq_a) + 1
        cols = len(seq_b) + 1
        matrix = np.zeros((rows, cols), dtype = int) #create data initialization with numpy zeros 

        for i in range(1, rows): #"i" will be assigned to rows
            matrix[i][0] = i * gap
        for j in range(1, cols): #"j" will be assigned to columns
            matrix[0][j] = j * gap

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

        #Get the diagonal score
        rows, cols = matrix.shape
        for i in range(1, rows): 
            for j in range(1, cols):
                if seq_a[i-1] == seq_b[j-1]: #a -> i, b -> j
                    score_di = matrix[i-1, j-1] + match
                else:
                    score_di = matrix[i-1, j-1] + mismatch 
        #Set gap scoring parameters:
                score_up = matrix[i-1, j] + gap 
                score_left = matrix[i, j-1] + gap 

                best_score = max(score_di, score_up, score_left)
                matrix[i, j] = best_score
        return matrix 

    def view_traceback(
        self, 
        matrix: np.ndarray,
        seq_a: str, 
        seq_b: str,
        match: int,
        mismatch: int,
        gap: int
    ) -> np.ndarray:

        i, j = matrix.shape[0] - 1, matrix.shape[1] - 1 
        #this made me mad because it gave me so many errors
        seq_align_a = []
        seq_align_b = []

        while i > 0 or j > 0:
            if i == 0:
                seq_align_a.append("-")
                seq_align_b.append(seq_b[j-1])
                j -= 1
                continue
            if j == 0:
                seq_align_a.append(seq_a[i-1])
                seq_align_b.append("-")
                i -= 1
                continue

            current = matrix[i, j]
            diag = matrix[i-1, j-1]
            up = matrix[i-1, j]
            left = matrix[i, j-1]

            if seq_a[i-1] == seq_b[j-1]:
                score_di = diag + match
            else:
                score_di = diag + mismatch

            score_up = up + gap
            score_left = left + gap 

            if current == score_di:
                seq_align_a.append(seq_a[i - 1])
                seq_align_b.append(seq_b[j - 1])
                i -= 1
                j -= 1
            elif current == score_up:
                seq_align_a.append(seq_a[i - 1])
                seq_align_b.append("-")
                i -= 1
            else: # go left:
                seq_align_a.append("-")
                seq_align_b.append(seq_b[j - 1])
                j -= 1

        seq_align_a.reverse()
        seq_align_b.reverse()

        return(seq_align_a, seq_align_b)

#Make sure to get the consensus sequence (best aligning) amongst the two (N as placeholder)
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

# TESTING/TROUBLESHOOTING CLASS CALLING AND INPUT PROCESSING THROUGH FUNCTIONS

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


#Pseudocode: 
#Consider putting everything into a class?
#Make sure to get all the input parameters
#Parameters should include:
    #sequence 1
    #sequence 2
    #match score
    #mismatch score
    #gap penalties
#Take all passed input/output from parsing.py
#Initialize the matrix and get it formatted for printing
#Functions should include: 
    #Matrix initialization 
    #Matrix construction
    #Matrix annotating/traceback
    #Matrix printing

#Questions: 
    #How will the parsing.py output be returned? 
    #How can the matrix initialization function take and utilize all parameters?
    #How do I fully utilize numpy for this? It appears to be necessary
    #Should re be imported for regex commands and fine-tuning?
    #What other modules should I import for this? 

#Citations: 
#numpy info: https://www.w3schools.com/python/numpy/numpy_creating_arrays.asp


#Ideas for other modules/main to discuss with team:
    #We will definitely want to have a CLI developed in one of the functions
    #Import argparse in this function

#2/19/2026
# def scrolling_output():
#     """
#         Purpose: Create image and table output for user
#         Input: Scoring matrix file 
#         Output: Image (likely .png), and a file (.csv or .tsv) of top three choices 
#         High-level steps: 
#         -    Create image formatting for the raw input data alongside the scoring and optimal traceback paths 
#         -    Export the image in a viewable, legible format 
#             .png, jpeg, .pdf 

#     """
#     pass

#     #Em will be doing the scrolling output function(s)