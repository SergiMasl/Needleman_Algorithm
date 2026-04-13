# Group 7 project: Needleman Algorithm

## URL: https://github.com/SergiMasl/Needleman_Algorithm


------------------------------------------------------------------------------------------------------------------------------------------

## Team Members:

### Em Scott

escott60@charlotte.edu
801453399

### Sergey Maslinikov

smaslini@charlotte.edu
801454115

### Mehrnoush Fereydouni

mfereydo@charlotte.edu
801311759

### Alyssa Leite

aleite@charlotte.edu
801495851

------------------------------------------------------------------------------------------------------------------------------------------

## General Information

This project was created for bioinformatics and genomics-related purposes, aligning two nucleotide sequences to find the most optimal alignment pathways. A consensus sequence is created from the two aligned sequences after alignment and given as an output to the user’s terminal. A .pdf output is also reported after program execution and written to "reports".


Executing the program is simple: Navigate to the Needleman_algorithm folder using your UNIX-supporting terminal, activate the .yml environment, and execute main.py after downloading the program. (Implement Bash script?) 

------------------------------------------------------------------------------------------------------------------------------------------

## Program Files

-main.py: Manages and coordinates all program modules, and is responsible for message execution to the terminal after the program runs. Contains the command-line interface for taking arguments. 

-input.py: Gathers user input for two sequences to be aligned, or permits for two .fasta file inputs, given the user’s choice. Located in the input_lib folder alongside an __init__ file for modularization. 

-validation.py: Makes sure that the nucleotide sequences contain valid characters and if provided .fasta input, cleans the sequences for further processing. Located in the validation_lib folder alongside an __init__ file for modularization.

-get_scoring_parameters.py: Asks the user whether the program’s default scoring parameters should be used. If the user wants to input their own scoring parameters, they may choose to do so. Located in the parsing_lib folder with an __init__ file for modularization. 

-parsing.py: Puts two DNA sequences in a table-like array for further processes. If the sequence lengths are not equal, the module is able to compensate and optimize during array creation. Located in the parsing_lib folder with an __init__ file for modularization.

-scrolling_output.py: Fills in the table-like array, using the scoring parameters either provided by default or given by the user. Performs the traceback to find the optimal sequence alignment, using the highest values during each traceback step. Located in the scrolling_output_lib folder with an __init__ file for modularization.

-report.py: Prints out the filled table-like array as a .pdf for user visualization of the algorithm process and alignment. Also calculates the program’s running time. Located in the Located in the report_lib folder with an __init__ file for modularization.

------------------------------------------------------------------------------------------------------------------------------------------


## License Information 

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

The GPL-3.0 is a strong copyleft license that ensures this gene comparison software and any modified or redistributed versions remain open source. We chose this license to promote transparency, reproducibility, and collaboration in bioinformatics research, while preventing proprietary use of the code.

------------------------------------------------------------------------------------------------------------------------------------------

## Environment Setup 

1. Install Anaconda
2. Clone the repository using git clone 
3. Create environment:
   conda env create -f environment.yml
4. Activate environment:
   conda activate needleman_algorithm
5. Run program:
   python main.py

------------------------------------------------------------------------------------------------------------------------------------------

## Dependencies

The Needleman-Wunsch Algorithm Program has a few dependencies that must be installed on either the local machine where the program is executed, or within a Conda environment. The most convenient way to execute the program is to run “conda activate needleman_algorithm” on the local machine’s terminal with either Miniconda or Anaconda installed. The imported dependencies are listed and described below: 


## Main Program

# python=3.11

- Python 3.11 is needed, as it is the main language of this program and needed to run the code/syntax properly. 


# NumPy

- NumPy has been utilized for the creation and initialization of matrices. For creating the output table in the scrolling_output.py module, NumPy is needed and preferred as it can perform the basic function of creating the initialized matrix, ready to be filled in with passed data from the parsing.py program.


------------------------------------------------------------------------------------------------------------------------------------------


## Citations:

*All citations are APA Formatted:*

#NumPy info: 

NumPy Creating Arrays. (n.d.). Www.w3schools.com. https://www.w3schools.com/python/numpy/numpy_creating_arrays.asp


#General Research: 

Timur, A. (2024). Needleman-Wunsch-Algorithm [Review of Needleman-Wunsch-Algorithm]. GitHub; Abdulkerim Talha Timur. Retrieved 2 C.E., from https://github.com/ATalhaTimur/Needleman-Wunsch-Algorithm

Anandakumar, M (2020, July 5). Needleman-Wunsch algorithm for DNA sequence alignment. Medium. https://medium.com/@amithunjha/needleman-wunsch-algorithm-for-dna-sequence-alignment-b103b8454de0

Khatizah, E., Nam, H.-J., & Park, H.-S. (2023). A Python-based educational software tool for visualizing bioinformatics alignment algorithms. Genomics & Informatics, 21(1), e15. https://doi.org/10.5808/gi.22055

Rashed, A. E. E.-D., Amer, H. M., El-Seddek, M., & Moustafa, H. E.-D. (2021). Sequence Alignment Using Machine Learning-Based Needleman–Wunsch Algorithm. IEEE Access, 9, 109522–109535. https://doi.org/10.1109/access.2021.3100408

Slowikowski, K. (n.d.). slowkow/needleman-wunsch.py GitHub Gist. Retrieved April 13, 2026, from https://gist.github.com/slowkow/06c6dba9180d013dfd82bec217d22eb5

Anonymous (2019). argparse — Parser for command-line options, arguments and sub-commands — Python 3.7.3 documentation. Python.org. https://docs.python.org/3/library/argparse.html

Anonymous (n.d.). __main__ — Top-level code environment — Python 3.10.4 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/__main__.html

Lord, D. (n.d.). click /README.md GitHub. Retrieved April 13, 2026, from https://github.com/pallets/click/blob/main/README.md

Sujay, A. (2025). GitHub - ahishsujay/Sequence_Alignment: Python script for global and local sequence alignment. GitHub. https://github.com/ahishsujay/Sequence_Alignment
