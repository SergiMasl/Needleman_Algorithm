#!/usr/bin/env python3

#escott60@charlotte.edu
#Em Scott (Updated 3/19/2026)

import numpy as np #give abbreviation to numpy
import sys
#from parsing_lib.parsing import (the parsing return)
#import 

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

        for i in range(1, rows):
            matrix[i][0] = i * gap

        for i in range(1, cols):
            matrix[j][0] = j * gap

        #export to main to show the step of the initialization? 

        return matrix


    def matrix_construct(
        self, 
        matrix: np.ndarray,
        seq1_array: np.ndarray, 
        seq2_array: np.ndarray,
        match: int, #get the defaults from CLI, implement getting user-specified parameters later
        mismatch: int, 
        gap: int
    ) -> np.ndarray:

        rows, cols = matrix.shape

        for i in range(1, rows): 
            for j in range(1, cols):
                if seq_a[i-1] == seq_b[j-1]:
                    diagonal = matrix[i-1][j-1] + match
                else:
                    diagonal = matrix[i-1][j-1] + mismatch


    #def view_traceback():

    #def matrix_print(): #print the formatted output, last function to code 

call_grid = GridBuild()
matrix = call_grid.matrix_init("AGATCATCTATCTA", "AGATCATCTGTACATT") #sample
print(matrix)

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
