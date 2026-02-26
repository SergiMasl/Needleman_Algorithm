#!/usr/bin/env python3

#escott60@charlotte.edu
#Em Scott

# Each student must choose and code at least one function for their final project today. 
# Update the GitHub/GitLab project. Uploaded the project here as a single compressed file.

import numpy as np #give abbreviation to numpy

class GridBuild():

    def matrix_init(self, seq_a: str, seq_b: str) -> tuple: #set up the matrix for printing
        """
        Purpose: Initialize a matrix with the sequences, getting it ready for output

        Parameters: Take the input cleaned sequences and create a grid based on the size
        
        Returns: Return a tuple containing initialized rows and columns
        """
        top_row = len(seq_a) + 1
        left_col = len(seq_b) + 1

        matrix = np.zeros((top_row, left_col), dtype = int) #create data initialization with numpy zeros 
        return matrix

    #def matrix_construct(seq_a: str, seq_b: str, match_score: int, mismatch_score: int, gap_penalties: int): #fill in the matrix with the returned parsing.py data

    #def view_traceback():

    #def matrix_print(): #print the formatted output, last function to code 

call_grid = GridBuild()
matrix = call_grid.matrix_init("AGATCATCTATCTA", "AGATCATCTGTACATT")
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