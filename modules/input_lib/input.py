#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alyssa Leite aleite@charlotte.edu 

input.py
Supports FASTA file input and inline sequence strings for Needleman-Wunsch global alignment tool.
Returns False on any error for next module to handle.
"""

import sys
from dataclasses import dataclass
from modules.validation_lib.validation import validate_dna_sequence, validate_fasta_dna


@dataclass
class SequenceInput:
    """
    Dataclass "SequenceInput" that stores the two DNA sequences and their names (or attributes).
    This is what gets passed to main.py to then move forward into: 
        - parsing.py (uses seq_a, seq_b to build the scoring matrix)
        - scrolling_output (uses seq_a, seq_b for traceback display)
        - report.py (uses seq_a, seq_b labels for PDF output)
    """
    seq_a: str
    seq_b: str
    label_a: str
    label_b: str


def parse_fasta_file(file: str) -> Tuple[str, str]:
    """
    Opens a FASTA file and reads the first DNA sequence inside it.
    Returns (label, sequence) or False if something goes wrong.
    Handles one file at a time. 

    Args: 
        file (str): Path to a FASTA or .fna file to be read. 

    Returns: 
        tuple[str, str]: A tuple of (label, sequence) where label is
            the FASTA header line (without '>') and sequence is the full
            DNA string with whitespace removed. 
        False: If the file is not found or is empty. 

    Raises: 
        FileNotFoundError: If the file path does not exist on disk. 
            Caught internally - returns False instead of crashing. 
    """
    # Use of the try/except block, this code is trying to open the file
    # but if it doesnt exist, it won't crash and will print an error message 
    # and return False. 
    try:
        fasta_file = open(file, "r")
        lines = fasta_file.readlines()
        fasta_file.close()
    except FileNotFoundError:
        sys.stderr.write(f"[Error] Could not find file: {file}\n")
        return False

    if len(lines) == 0:
        sys.stderr.write(f"[Error] File is empty: {file}\n")
        return False

    
    label = file
    start = 0

    # Setting the header as the label of the sequence
    if lines[0].startswith(">"):
        label = lines[0][1:].strip()
        start = 1

    # Looping through remaining lines and building the sequence string. 
    # Stops if it hits another > (which indicates the second sequence in file)
    sequence = ""
    for line in lines[start:]:
        if line.startswith(">"):
            break
        sequence = sequence + line.strip()

    return label, sequence


def read_two_fastas(file1: str, file2: str)-> Tuple[str, str, str, str]:
    """
    Reads two separate FASTA files and returns both sequences and their labels.
    Calls parse_fasta_file() on each file individually, and calls it twice. 
    Returns False if either file fails to parse.

    Args: 
        file1 (str): Path to the first FASTA file (sequence A).
        file2 (str): Path to the second FASTA file (sequence B).

    Returns: 
        tuple[str, str, str, str]: A tuple of (label_a, seq_a, label_b, seq_b)
            where label_a and label_b are the FASTA header strings, and seq_a
            and seq_b are the full DNA sequences as strings. 
        False: If either fails to parse. 

    Raises: 
        No exceptions raised directly, errors are handled inside 
        parse_fasta_file() and returned as False. 
    """
    # Is calling parse_fasta_file() function twice, once per file. If either
    # one fails, it returns False without continuing. 
    result_a = parse_fasta_file(file1)
    result_b = parse_fasta_file(file2)

    if result_a is False or result_b is False:
        return False

    # Unpacking both results from parse_fasta_file and return all four values as a tuple. 
    label_a, seq_a = result_a
    label_b, seq_b = result_b

    return label_a, seq_a, label_b, seq_b


def build_sequence_input(raw_a: str, raw_b: str, label_a: str, label_b: str) -> SequenceInput:
    """
    Validates both DNA sequences and packages them into a SequenceInput dataclass. 
    Delegates validation to validation.py. 
    Returns False if either sequence contains invalid characters.

    Args: 
        raw_a (str): Raw DNA sequence string for sequence A. 
        raw_b (str): Raw DNA sequence string for sequence B. 
        label_a (str): Display label for sequence A, used in error messages 
        and output visualization. 
        label_b (str): Display label for sequence B, used in error messages 
        and output visualization. 

    Returns: 
        SequenceInput: A dataclass containing validated seq_a, seq_b, label_a, 
        and label_b that are ready to be passed to parsing.py. 
        False: If either sequence fails DNA validation. 

    Raises: 
        ValueError: If either sequence is empty or contains characters other 
        than A, C, G, T. Caught internally, returns False instead of crashing. 
    """
    # Use of a try/except block to run both sequences through validation.py module. If either
    # has invalid characters, it riases a ValueError. 
    try:
        seq_a = validate_dna_sequence(raw_a, name=label_a)
        seq_b = validate_dna_sequence(raw_b, name=label_b)
    except ValueError as error:
        # Catches the error, prints it, and returns False instead of crashing. 
        sys.stderr.write(f"[Error] {error}\n")
        return False
    # If everything passed validation, packages it all into a SequenceInput object and returns it. 
    return SequenceInput(seq_a=seq_a, seq_b=seq_b, label_a=label_a, label_b=label_b)


def input_sequences(args: argparse.NameSpace)-> SequenceInput:
    """
    Asks the user whether to load sequences from a FASTA file or type them manually.
    Returns a SequenceInput object, or exits on error.
    """
    # Asking user if they want to provide sequences, and will keep asking until user provides "fasta" or "manual".
    choice = input("Do you want to load sequences from a FASTA file or type them manually? (fasta/manual): ")
    while choice.lower() not in ["fasta", "manual"]:
        choice = input("Invalid input. Please enter 'fasta' or 'manual': ")

    # If user chose FASTA, prompts for two file paths, parses each one, and re-asks on failure.
    if choice.lower() == "fasta":
        while True:
            file_path_a = input("Enter full path to first FASTA file: ").strip()
            parsed_a = parse_fasta_file(file_path_a)
            if parsed_a is False:
                retry = input("File not found or empty. Try again or exit? (retry/exit): ").strip().lower()
                while retry not in ["retry", "exit"]:
                    retry = input("Please enter 'retry' or 'exit': ").strip().lower()
                if retry == "exit":
                    sys.exit(1)
                continue
            label_a, raw_a = parsed_a
            seq_a = validate_fasta_dna(file_path_a, raw_a, label_a)
            if seq_a is not False:
                break

        while True:
            file_path_b = input("Enter full path to second FASTA file: ").strip()
            parsed_b = parse_fasta_file(file_path_b)
            if parsed_b is False:
                retry = input("File not found or empty. Try again or exit? (retry/exit): ").strip().lower()
                while retry not in ["retry", "exit"]:
                    retry = input("Please enter 'retry' or 'exit': ").strip().lower()
                if retry == "exit":
                    sys.exit(1)
                continue
            label_b, raw_b = parsed_b
            seq_b = validate_fasta_dna(file_path_b, raw_b, label_b)
            if seq_b is not False:
                break

        result = build_sequence_input(seq_a, seq_b, label_a, label_b)
    # If user chose manual, prompts for two raw sequences and gives them default labels "seq1" and "seq2".
    else:
        while True:
            raw_a = input("Enter first DNA sequence (A, T, C, G only): ").strip()
            try:
                validate_dna_sequence(raw_a, name="seq1")
                break
            except ValueError as error:
                sys.stderr.write(f"[Error] {error}\n")

        while True:
            raw_b = input("Enter second DNA sequence (A, T, C, G only): ").strip()
            try:
                validate_dna_sequence(raw_b, name="seq2")
                break
            except ValueError as error:
                sys.stderr.write(f"[Error] {error}\n")

        result = build_sequence_input(raw_a, raw_b, "seq1", "seq2")

    # Final check: if anything failed, exit. Otherwise return the SequenceInput object to be used by program. 
    if result is False:
        sys.exit(1)
    return result
