"""
validation.py

Validate DNA sequences and basic integer inputs before running
the Needleman-Wunsch alignment algorithm.

Features:
- Cleans sequences (remove whitespace, convert to uppercase)
- Ensures sequences contain only A, C, G, T
- Validates integer inputs when needed
"""
# Updated by: Mehrnoush Fereydouni: April 9, 2026
# Changes:
# - Replaced bare except with 'except Exception'
# - Added type hints to validate_int and validate_scoring
# - Improved DNA validation error message
# - Expanded validate_scoring docstring for consistency


# Allowed DNA characters
VALID_DNA = {"A", "C", "G", "T"}


def normalize_sequence(seq: str | None) -> str:
    """
    Clean a DNA sequence by removing whitespace and converting to uppercase.

    Args:
        seq: Raw input DNA sequence.

    Returns:
        Cleaned DNA sequence as an uppercase string.
    """
    if seq is None:
        return ""
    return "".join(seq.split()).upper()


def validate_dna_sequence(seq: str | None, name: str = "sequence") -> str:
    """
    Validate a DNA sequence (A, C, G, T only).

    Args:
        seq: Input DNA sequence.
        name: Label used in error messages.

    Returns:
        Cleaned, validated DNA sequence.

    Raises:
        ValueError: If the sequence is empty or contains invalid characters.
    """
    cleaned = normalize_sequence(seq)

    # Check for empty sequence
    if cleaned == "":
        raise ValueError(
            f"{name} is empty. Please enter a DNA sequence using only A, C, G, and T."
        )

    invalid_chars = sorted(set(cleaned) - VALID_DNA)
    if invalid_chars:
        raise ValueError(
            f"{name} contains invalid character(s): {', '.join(invalid_chars)}. "
            "Only A, C, G, and T are allowed."
        )

    return cleaned


def validate_int(value: object, name: str) -> int:
    """
    Validate that a value can be converted to an integer.

    Args:
        value: Input value.
        name: Label used in error messages.

    Returns:
        Integer form of the value.

    Raises:
        ValueError: If the value is not a valid integer.
    """
    try:
        return int(value)
    except Exception:
        raise ValueError(f"{name} must be an integer. You entered: {value}")


def validate_scoring(match: int, mismatch: int, gap: int) -> tuple[int, int, int]:
    """
    Validate scoring configuration before alignment.

    Args:
        match: Match score.
        mismatch: Mismatch score.
        gap: Gap penalty.

    Returns:
        Tuple of validated scoring values (match, mismatch, gap).

    Raises:
        ValueError: If all scoring values are zero.
    """
    if match == 0 and mismatch == 0 and gap == 0:
        raise ValueError(
            "Scoring cannot be all zeros; alignment would be meaningless."
        )

    return match, mismatch, gap


# Mehrnoush will be doing the validation function(s)

