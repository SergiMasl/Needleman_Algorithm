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
