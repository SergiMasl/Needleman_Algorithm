# Group 7 project: Needleman Algorithm


## Needleman Algorithm:

Build a recursive tool that aligns two DNA sequences, takes input match, mismatch, and gap penalties, and can create a graph to visualize the best path (Needleman-Wunsch)


## General explanation:

Create an algorithm that can score global DNA alignments in a data table-like fashion, and
be capable of performing a traceback. The algorithm will be executable with Python3 and 
Bash commands


## Clear objective:

Be able to input/read two DNA sequences

Compare information (similarities vs differences) between the two sequences
Report the most optimal alignment(s)

Be capable of tracing back from the data table’s endpoint (bottom-right corner)
Go from being a data table to a visualized depiction

Upon entering the GUI, the user is given a very simple and concise guideline on how to use this software.

However, code for potential exceptions. Invalid inputs should result in error messages and prompts to enter in valid characters.

The error messages should give examples or a list of valid characters (Integers, alphanumerics, etc.)


## List of core functionalities:

This program should be able to align two input sequences, recognize gaps, matches, and mismatches, and apply a user-determined scoring system. 

The user interface should accommodate functionality and purpose of the program

Input data should be put in a data table (much like the R data type) and be parsed through to determine the best alignment path

Default scoring systems *should* be provided in case the user doesn’t know what they’re doing.

Novel and experimental scoring options should be provided in an “advanced” settings” button that can be toggled for extra user input

After parsing through the aligned sequences, a visualization is the final output, but the program needs to have the option to retry/restart the sequencing. 

If time allows, a cache of prior-used sequences should be stored for accessibility and user-friendliness. 


# Expected outcome:

The program will allow users to easily determine and understand what portions of their two sequences are homologous

The scoring system is flexible and allows user input, allowing conventional scoring methods or novel, experimental ones

Ranked homologs are given to the user in a concise, visually-friendly manner. The interface is very simple, clear, and easily understandable with design choices

The program is streamlined, free of bugs, and does not have considerable lag. 
The majority, if not all of the program, can be used offline.

This project should be able to process multiple user inputs and create simple-yet-effective visual results for easy understanding. The program should be able to rank optimal paths and tie them as well via score calculations