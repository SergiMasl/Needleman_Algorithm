
"""
validation.py


- Cleans sequences (remove whitespace, convert to uppercase)
- Ensures sequences contain only A, C, G, T
- Validates scoring values (match, mismatch, gap)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Set


# Allowed DNA characters
VALID_DNA: Set[str] = {"A", "C", "G", "T"}


def normalize_sequence(seq: str) -> str:
    """
    Clean a DNA sequence by removing whitespace and converting to uppercase.
    """
    if seq is None:
        return ""
    return "".join(seq.split()).upper()


def validate_dna_sequence(seq: str, name: str = "sequence") -> str:
    """
    Validate a DNA sequence (A/C/G/T only).
    Raises an error if the sequence is empty or contains invalid characters.
    """
    cleaned = normalize_sequence(seq)

    if cleaned == "":
        raise ValueError(
            f"{name} is empty. Please enter a DNA sequence using A, C, G, T."
        )

    invalid_chars = sorted(set(cleaned) - VALID_DNA)
    if invalid_chars:
        raise ValueError(
            f"{name} contains invalid character(s): {', '.join(invalid_chars)}. "
            "Allowed characters: A, C, G, T."
        )

    return cleaned


def validate_int(value: str, name: str) -> int:
    """
    Validate that a value can be converted to an integer.
    """
    try:
        return int(value)
    except Exception:
        raise ValueError(f"{name} must be an integer. entered: {value!r}")


@dataclass(frozen=True)
class ScoringScheme:
    """
    Store scoring parameters for Needleman–Wunsch alignment.
    """
    match: int = 1
    mismatch: int = -1
    gap: int = -2


def validate_scoring(match: int, mismatch: int, gap: int) -> ScoringScheme:
    """
    Validate scoring configuration before alignment.
    """
    if match == 0 and mismatch == 0 and gap == 0:
        raise ValueError(
            "Scoring cannot be all zeros; alignment would be meaningless."
        )

    return ScoringScheme(match=match, mismatch=mismatch, gap=gap)


# Mehrnoush will be doing the validation function(s)
