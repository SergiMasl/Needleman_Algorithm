# Group 7 project: Needleman Wunsch Algorithm Tool

## URL: https://github.com/SergiMasl/Needleman_Algorithm


------------------------------------------------------------------------------------------------------------------------------------------

## Team Members:

### Em Scott

escott60@charlotte.edu
801453399
GitHub: escott60

### Sergey Maslinikov

smaslini@charlotte.edu
801454115
GitHub: SergiMasl

### Mehrnoush Fereydouni

mfereydo@charlotte.edu
801311759
GitHub: MehrnoushF

### Alyssa Leite 
aleite@charlotte.edu
801495851
GitHub: agleite19

-----------------------------------------------------------------------------------------------------------------------------------------

# General Information: Needleman Wunsch Algorithm Tool

The Needleman-Wunsch Algorithm Tool is a start-to-finish Python implementation of the Needleman-Wunsch global alignment algorithm for pairwise alignment of two DNA sequences. It accepts input as either raw inline sequences or standard FASTA files, constructs a complete scoring matrix using default or user-defined match, mismatch, and gap parameters, and performs a full traceback to determine the most optimal alignment pathway. A consensus sequence is derived from the two aligned sequences and reported directly to the terminal via scrolling output. A formatted .csv report and a .pdf report containing the scoring matrix and sequence statistics is automatically generated and saved to `__Reports/` upon program completion.

Executing the program is straightforward: clone the repository, create and activate the provided Conda environment `(needleman_algorithm)`, and run python `main.py` from the project root. A bash script `(run_alignment.sh)` is also provided for streamlined execution with predefined input sequences and scoring parameters.

------------------------------------------------------------------------------------------------------------------------------------------

# Program Files

`main.py`: Manages and coordinates all program modules, and is responsible for message execution to the terminal after the program runs. Contains the command-line interface for taking arguments. 

`input.py`: Gathers user input for two sequences to be aligned, or permits for two .fasta file inputs, given the user’s choice. Located in the `input_lib` folder alongside an `__init__` file for modularization. 

`validation.py`: Makes sure that the nucleotide sequences contain valid characters and if provided .fasta input, cleans the sequences for further processing. Located in the `validation_lib` folder alongside an `__init__` file for modularization.

`get_scoring_parameters.py`: Asks the user whether the program’s default scoring parameters should be used. If the user wants to input their own scoring parameters, they may choose to do so. Located in the `parsing_lib` folder with an `__init__` file for modularization. 

`parsing.py`: Puts two DNA sequences in a table-like array for further processes. If the sequence lengths are not equal, the module is able to compensate and optimize during array creation. Located in the `parsing_lib` folder with an `__init__` file for modularization.

`scrolling_output.py`: Fills in the table-like array, using the scoring parameters either provided by default or given by the user. Performs the traceback to find the optimal sequence alignment, using the highest values during each traceback step. Located in the `scrolling_output_lib` folder with an `__init__` file for modularization.

`report.py`: Prints out a .csv and a filled table-like array as a .pdf for user visualization of the algorithm process and alignment. Also calculates the program’s running time. Located in the `report_lib` folder with an `__init__` file for modularization.

------------------------------------------------------------------------------------------------------------------------------------------
# Input Options

The tool accepts two DNA sequences via one of two modes, selected interactively at runtime.

**Manual (inline)**

Type sequences directly into the terminal when prompted. Sequences must contain only `A`, `C`, `G`, and `T` — lowercase is accepted and automatically converted to uppercase. Whitespace is stripped automatically.

```
Enter first DNA sequence (A, T, C, and G only):  AGATCATCTA
Enter second DNA sequence (A, T, C, and G only): AGATCATCTG
```

**FASTA file**

Provide the full path to two separate `.fasta` or `.fna` files, one per sequence. Each file must contain at least one sequence. Only the first sequence in each file is read. The header line (`>`) is optional — if present, it is used as the sequence label in the output report.

```
>seq1
AGATCATCTA
```
------------------------------------------------------------------------------------------------------------------------------------------
## Output Files

**Reports** (`__Reports/<filename>.csv`, `__Reports/<filename>.pdf`)

A .csv file and a .pdf file are generated automatically after every run and saved to the `__Reports/` folder in the project root. 

The .csv file contains a report of the scoring parameters, input sequences, alignment with the consensus sequence and alignment score, and the scoring matrix.   

The .pdf report contains two pages: a scoring matrix table with match/mismatch/gap parameters labeled, and a sequence statistics page showing length and GC content for both sequences. The default filename is a timestamp (`YYYY-MM-DD_HH-MM-SS.pdf`). A custom name can be passed with `--outputpdf`.

**Terminal Output**

The terminal output includes the aligned sequences (`Aligned A` and `Aligned B`) along with the consensus sequence of the alignment. It also prints the filepath of the `.csv` and the `.pdf`. 


------------------------------------------------------------------------------------------------------------------------------------------

# Command Line Interface Options

For default parameters, input into command line: 
```bash
python main.py
```
A prompt will appear asking if user wants to keep default parameters or not. 



For non-default parameters, A command line interface (CLI) has been added to `main.py` for optimal handling of input arguments if the user chooses to. The CLI information is listed below:

| Flag | Long Form | Default | Description |
|------|-----------|---------|-------------|
| `-i` | `--firstseq` | None | The first uploaded sequence, denoted as "i" |
| `-j` | `--secondseq` | None | The second uploaded sequence, denoted as "j" |
| `-f` | `--inputfasta` | `sequences.fasta` | FASTA file inputs for parsing, cleaning, and validation |
| `-m` | `--match` | `2` | Match score parameter in the case that two nucleotide sequences align |
| `-n` | `--mismatch` | `-1` | Mismatch score parameter in the case that two nucleotide sequences do not align |
| `-g` | `--gapscore` | `-2` | Gap score parameter in the case that there is a gap in one sequence or both sequences |
| `-o` | `--outputpdf` | timestamp | Output file argument, formatted as a `.pdf` for easy accessibility, printing, and documentation |

### Example Usage for Customized Parameters
```bash
python main.py --match 2 --mismatch -1 --gapscore -2 --outputpdf my_alignment.pdf
```
 ------------------------------------------------------------------------------------------------------------------------------------------

# License Information 

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

The GPL-3.0 is a strong copyleft license that ensures this gene comparison software and any modified or redistributed versions remain open source. We chose this license to promote transparency, reproducibility, and collaboration in bioinformatics research, while preventing proprietary use of the code.

------------------------------------------------------------------------------------------------------------------------------------------

# Environment Setup

1. Install [Miniconda](https://docs.anaconda.com/miniconda/) or [Anaconda](https://www.anaconda.com/download)

2. Clone the repository:
```bash
git clone https://github.com/SergiMasl/Needleman_Algorithm.git
```

3. Create the conda environment:
```bash
conda env create -f environment.yml
```

4. Activate the environment:
```bash
conda activate needleman_algorithm
```

5. Run the program:
```bash
python main.py
```
------------------------------------------------------------------------------------------------------------------------------------------

# Dependencies

The Needleman-Wunsch Algorithm Program has a few dependencies that must be installed on either the local machine where the program is executed, or within a Conda environment. The most convenient way to execute the program is to run “conda activate needleman_algorithm” on the local machine’s terminal with either Miniconda or Anaconda installed. The imported dependencies are listed and described below: 


## Main Program

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.11 | Core language required to run the program |
| NumPy | latest | Matrix creation and initialization for the scoring table |
| Matplotlib | latest | Generates the PDF alignment report |
| Numba | latest | Speeds up calculations in `scrolling_output.py`; note the first run is slower due to initial compilation |

1. Python 3.11 is needed, as it is the main language of this program and needed to run the code/syntax properly. 

2. NumPy has been utilized for the creation and initialization of matrices. For creating the output table in the `scrolling_output.py` module, NumPy is needed and preferred as it can perform the basic function of creating the initialized matrix, ready to be filled in with passed data from the `parsing.py` program.

3. MatPlotLib is needed to create a formatted, readable alignment output for the program user to view. The .pdf report of the user's alignment is easily downloadable, printable, and compressable in a .zip file if need be for sharing and space allocation.

4. Numba is used to help compile the speed of the calculations in `scrolling_output.py`. Initially during the first simple alignment, Numba takes extra time to compile and initialize. Thus, the first alignment should be smaller sequences. After this initial compilation, Numba will run optimally and assist in speeding up the algorithm. 

------------------------------------------------------------------------------------------------------------------------------------------


# Citations:

*All citations are APA Formatted:*

## NumPy info: 

NumPy Creating Arrays. (n.d.). Www.w3schools.com. https://www.w3schools.com/python/numpy/numpy_creating_arrays.asp

## Numba info:

A ~5 minute guide to Numba — Numba documentation. (2019). Pydata.org. https://numba.pydata.org/numba-doc/dev/user/5minguide.html



## General Research: 

Timur, A. (2024). Needleman-Wunsch-Algorithm [Review of Needleman-Wunsch-Algorithm]. GitHub; Abdulkerim Talha Timur. Retrieved 2 C.E., from https://github.com/ATalhaTimur/Needleman-Wunsch-Algorithm

Anandakumar, M (2020, July 5). Needleman-Wunsch algorithm for DNA sequence alignment. Medium. https://medium.com/@amithunjha/needleman-wunsch-algorithm-for-dna-sequence-alignment-b103b8454de0

Khatizah, E., Nam, H.-J., & Park, H.-S. (2023). A Python-based educational software tool for visualizing bioinformatics alignment algorithms. Genomics & Informatics, 21(1), e15. https://doi.org/10.5808/gi.22055

Rashed, A. E. E.-D., Amer, H. M., El-Seddek, M., & Moustafa, H. E.-D. (2021). Sequence Alignment Using Machine Learning-Based Needleman–Wunsch Algorithm. IEEE Access, 9, 109522–109535. https://doi.org/10.1109/access.2021.3100408

Slowikowski, K. (n.d.). slowkow/needleman-wunsch.py GitHub Gist. Retrieved April 13, 2026, from https://gist.github.com/slowkow/06c6dba9180d013dfd82bec217d22eb5

Anonymous (2019). argparse — Parser for command-line options, arguments and sub-commands — Python 3.7.3 documentation. Python.org. https://docs.python.org/3/library/argparse.html

Anonymous (n.d.). __main__ — Top-level code environment — Python 3.10.4 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/__main__.html

Lord, D. (n.d.). click /README.md GitHub. Retrieved April 13, 2026, from https://github.com/pallets/click/blob/main/README.md

Sujay, A. (2025). GitHub - ahishsujay/Sequence_Alignment: Python script for global and local sequence alignment. GitHub. https://github.com/ahishsujay/Sequence_Alignment

GeeksforGeeks. (2017, July 15). numpy.arange() in Python. GeeksforGeeks. https://www.geeksforgeeks.org/python/numpy-arrange-in-python/

GeeksforGeeks. (2025, February 6). Deque vs List in Python. GeeksforGeeks. https://www.geeksforgeeks.org/python/deque-vs-list-in-python/

Python Optional Argument. (2026). Mimo.org. https://mimo.org/glossary/python/optional-arguments

Dillinger. (n.d.). Dillinger - Online Markdown Editor [Software]. https://dillinger.io/


## AI Citation and Prompts: 

Claude.ai is cited for debugging help in the case of syntax and runtime errors. Prompts are listed below:

Anthropic. (2025). Claude. Claude.ai. https://claude.ai/

# Prompts:

-What is the best way to make sure I am using numba and calling on @njit in my script?

-With Needleman-Wunsch tie options, what methodology do I need to apply to Python to traceback a noticeably different alignment? 

-Double-checking the alignment logic and found an error in tie_traceback with rows and columns (i, j). 

-Do I need to call @staticmethod after adding Numba and calling @njit outside of my class script? 

-Format and explain corrections for the report docstrings:

-How to properly write a bash script to test a Python project

-How to properly format a README.md file to have a cleaner, more professional look