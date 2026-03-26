"""
validation.py

Validate DNA sequences and basic integer inputs before running
the Needleman-Wunsch alignment algorithm.

- Cleans sequences (remove whitespace, convert to uppercase)
- Ensures sequences contain only A, C, G, T
- Validates integer inputs when needed
"""

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

    if cleaned == "":
        raise ValueError(
            f"{name} is empty. Please enter a DNA sequence using only A, C, G, and T."
        )

    invalid_chars = sorted(c for c in set(cleaned) if not c.isalpha())
    if invalid_chars:
        raise ValueError(
            f"{name} contains invalid character(s): {', '.join(invalid_chars)}. "
            "Only alphabetic characters are allowed."
        )

    return cleaned


def validate_int(value, name: str) -> int:
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
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer. You entered: {value}")
