#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
validation.py

Validate DNA sequences and basic integer inputs before running
the Needleman-Wunsch alignment algorithm.

Features:
- Cleans sequences (remove whitespace, convert to uppercase)
- Ensures sequences contain only A, C, G, T
- Validates integer inputs when needed
"""

# Updated by: Mehrnoush Fereydouni
# Last Updated: April 23, 2026
# Changes:
# - Replaced bare except with 'except Exception'
# - Added type hints to validate_int and validate_scoring
# - Improved DNA validation error message
# - Expanded validate_scoring docstring for consistency


# Allowed DNA characters
VALID_DNA = {"A", "C", "G", "T"}


def normalize_sequence(seq: str | None) -> str:
    """
    Purpose:
        Clean a DNA sequence by removing whitespace and converting it to uppercase.

    Parameters:
        seq: Raw input DNA sequence.

    Returns:
        Cleaned DNA sequence as an uppercase string.

    Example:
        normalize_sequence("a c g t") -> "ACGT"
    """
    if seq is None:
        return ""
    return "".join(seq.split()).upper()


def validate_dna_sequence(seq: str | None, name: str = "sequence") -> str:
    """
    Purpose:
        Validate that a DNA sequence contains only valid nucleotides
        (A, C, G, and T).

    Parameters:
        seq: Input DNA sequence.
        name: Label used in error messages.

    Returns:
        Cleaned and validated DNA sequence.

    Raises:
        ValueError: If the sequence is empty or contains invalid characters.

    Example:
        validate_dna_sequence("acgt") -> "ACGT"
    """
    cleaned = normalize_sequence(seq)

    # Check for empty sequence
    if cleaned == "":
        raise ValueError(
            f"{name} is empty. Please enter a DNA sequence using only A, C, G, and T."
        )

    # Identify invalid DNA characters
    invalid_chars = sorted(set(cleaned) - VALID_DNA)
    if invalid_chars:
        raise ValueError(
            f"{name} contains invalid character(s): {', '.join(invalid_chars)}. "
            "Only A, C, G, and T are allowed."
        )

    return cleaned


def validate_fasta_loadable(file_path: str):
    """
    Purpose:
        Check that a FASTA file exists on disk and is not empty.
        If either check fails, reports the specific problem with the file path,
        then prompts the user to retry with a different file or exit.

    Parameters:
        file_path: Path provided by the user.

    Returns:
        True if the file exists and is non-empty.
        False if the user chooses to retry (caller should re-prompt for a new file).
        Calls sys.exit(1) if the user chooses to exit.

    Example:
        validate_fasta_loadable("seq1.fasta") -> True
    """
    import sys
    import os
    if not os.path.isfile(file_path):
        sys.stderr.write(f"[Error] File not found: '{file_path}'\n")
    elif os.path.getsize(file_path) == 0:
        sys.stderr.write(f"[Error] File is empty: '{file_path}'\n")
    else:
        return True
    retry = input("Re-enter the correct file path or exit? (retry/exit): ").strip().lower()
    while retry not in ["retry", "exit"]:
        retry = input("Please enter 'retry' or 'exit': ").strip().lower()
    if retry == "exit":
        sys.exit(1)
    return False


def validate_fasta_extension(file_path: str) -> bool:
    """
    Purpose:
        Check that a file path ends with the .fasta extension.
        If not, reports the error so the user can provide a correct file.

    Parameters:
        file_path: Path provided by the user.

    Returns:
        True if the extension is .fasta, False otherwise.

    Example:
        validate_fasta_extension("seq1.fasta") -> True
        validate_fasta_extension("seq1.txt")   -> False
    """
    if not file_path.lower().endswith(".fasta"):
        import sys
        sys.stderr.write(
            f"[Error] '{file_path}' is not a .fasta file. "
            "Please provide a file with a .fasta extension.\n"
        )
        return False
    return True


def validate_fasta_dna(file_path: str, raw_seq: str, label: str):
    """
    Purpose:
        Validate DNA from a parsed FASTA file.
        If the sequence contains invalid characters, reports which file is
        broken and why, then prompts the user to retry with a new file or exit.

    Parameters:
        file_path: Path to the FASTA file (used in the error message).
        raw_seq:   Raw sequence string read from the file.
        label:     FASTA header label (used in the error message).

    Returns:
        Cleaned, uppercase DNA string on success.
        False if the user chooses to retry (caller should re-prompt for a new file).
        Calls sys.exit(1) if the user chooses to exit.

    Example:
        validate_fasta_dna("seq1.fasta", "acgt", "seq1") -> "ACGT"
    """
    import sys
    try:
        return validate_dna_sequence(raw_seq, name=label)
    except ValueError as error:
        sys.stderr.write(f"[Error] File '{file_path}' is invalid: {error}\n")
        retry = input("Re-enter the correct file path or exit? (retry/exit): ").strip().lower()
        while retry not in ["retry", "exit"]:
            retry = input("Please enter 'retry' or 'exit': ").strip().lower()
        if retry == "exit":
            sys.exit(1)
        return False


def validate_single_fasta_sequence(file_path: str):
    """
    Purpose:
        Check that a FASTA file contains exactly one sequence (one '>' header).
        If more than one header is found, reports the file and the count,
        then prompts the user to retry with a different file or exit.

    Parameters:
        file_path: Path to the FASTA file to inspect.

    Returns:
        True if the file has exactly one sequence.
        False if the user chooses to retry (caller should re-prompt for a new file).
        Calls sys.exit(1) if the user chooses to exit.

    Example:
        validate_single_fasta_sequence("seq1.fasta") -> True
    """
    import sys
    try:
        with open(file_path, "r") as f:
            header_count = sum(1 for line in f if line.startswith(">"))
    except FileNotFoundError:
        return True  # parse_fasta_file already handles missing files

    if header_count > 1:
        sys.stderr.write(
            f"[Error] File '{file_path}' contains {header_count} sequences. "
            "Only 1 sequence per file is allowed.\n"
        )
        retry = input("Re-enter the correct file path or exit? (retry/exit): ").strip().lower()
        while retry not in ["retry", "exit"]:
            retry = input("Please enter 'retry' or 'exit': ").strip().lower()
        if retry == "exit":
            sys.exit(1)
        return False
    return True


def validate_int(value: object, name: str) -> int:
    """
    Purpose:
        Validate that a value can be converted to an integer.

    Parameters:
        value: Input value.
        name: Label used in error messages.

    Returns:
        Integer form of the value.

    Raises:
        ValueError: If the value is not a valid integer.

    Example:
        validate_int("2", "match") -> 2
    """
    try:
        return int(value)
    except Exception:
        raise ValueError(f"{name} must be an integer. You entered: {value}")


def validate_scoring(match: int, mismatch: int, gap: int) -> tuple[int, int, int]:
    """
    Purpose:
        Validate scoring configuration before alignment.

    Parameters:
        match: Match score.
        mismatch: Mismatch score.
        gap: Gap penalty.

    Returns:
        Tuple of validated scoring values (match, mismatch, gap).

    Raises:
        ValueError: If all scoring values are zero.

    Example:
        validate_scoring(2, -1, -2) -> (2, -1, -2)
    """
    if match == 0 and mismatch == 0 and gap == 0:
        raise ValueError(
            "Scoring cannot be all zeros; alignment would be meaningless."
        )

    return match, mismatch, gap


# Mehrnoush will be doing the validation function(s)
