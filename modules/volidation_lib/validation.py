"""
validation.py

Validate DNA sequences and scoring parameters before running
the Needleman-Wunsch alignment algorithm.

Features:
- Cleans sequences (removes whitespace, converts to uppercase)
- Ensures sequences contain only valid DNA characters: A, C, G, T
- Validates scoring values (match, mismatch, gap)
- Checks sequence length limits
- Returns cleaned and validated values ready for alignment
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

    if cleaned.startswith(">"):
        raise ValueError(
            f"{name} appears to include a FASTA header. Please provide only the DNA sequence."
        )

    invalid_chars = sorted(set(cleaned) - VALID_DNA)
    if invalid_chars:
        raise ValueError(
            f"{name} contains invalid character(s): {', '.join(invalid_chars)}. "
            "Allowed characters: A, C, G, T. Example valid sequence: ACGTACGT."
        )

    return cleaned


def validate_sequence_length(
    seq: str,
    name: str = "sequence",
    min_len: int = 1,
    max_len: int = 1000
) -> str:
    """
    Validate that a sequence length falls within the allowed range.

    Args:
        seq: Validated DNA sequence.
        name: Label used in error messages.
        min_len: Minimum allowed sequence length.
        max_len: Maximum allowed sequence length.

    Returns:
        The same sequence if valid.

    Raises:
        ValueError: If sequence length is outside the allowed range.
    """
    seq_len = len(seq)

    if seq_len < min_len:
        raise ValueError(
            f"{name} is too short. Minimum allowed length is {min_len}."
        )

    if seq_len > max_len:
        raise ValueError(
            f"{name} is too long. Maximum allowed length is {max_len}."
        )

    return seq


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
        raise ValueError(
            f"{name} must be an integer. You entered: {value}. "
            "Example valid values: 2, -1, -2."
        )


def validate_scoring(match, mismatch, gap) -> tuple[int, int, int]:
    """
    Validate scoring configuration before alignment.

    Args:
        match: Match score.
        mismatch: Mismatch score.
        gap: Gap penalty.

    Returns:
        Tuple of validated integers: (match, mismatch, gap)

    Raises:
        ValueError: If the scoring system is invalid.
    """
    match = validate_int(match, "match")
    mismatch = validate_int(mismatch, "mismatch")
    gap = validate_int(gap, "gap")

    if match == 0 and mismatch == 0 and gap == 0:
        raise ValueError(
            "Scoring cannot be all zeros; alignment would be meaningless."
        )

    if match <= 0:
        raise ValueError("Match score should be a positive integer.")

    if gap > 0:
        raise ValueError("Gap penalty should usually be zero or negative.")

    if mismatch > match:
        raise ValueError(
            "Mismatch score should not be greater than the match score."
        )

    return match, mismatch, gap


def validate_alignment_input(
    seq1,
    seq2,
    match,
    mismatch,
    gap,
    min_len: int = 1,
    max_len: int = 1000
) -> tuple[str, str, int, int, int]:
    """
    Validate and normalize all alignment inputs together.

    Args:
        seq1: First DNA sequence.
        seq2: Second DNA sequence.
        match: Match score.
        mismatch: Mismatch score.
        gap: Gap penalty.
        min_len: Minimum allowed sequence length.
        max_len: Maximum allowed sequence length.

    Returns:
        Tuple of validated values:
        (clean_seq1, clean_seq2, match, mismatch, gap)

    Raises:
        ValueError: If any sequence or scoring input is invalid.
    """
    seq1 = validate_dna_sequence(seq1, "Sequence 1")
    seq2 = validate_dna_sequence(seq2, "Sequence 2")

    seq1 = validate_sequence_length(seq1, "Sequence 1", min_len, max_len)
    seq2 = validate_sequence_length(seq2, "Sequence 2", min_len, max_len)

    match, mismatch, gap = validate_scoring(match, mismatch, gap)

    return seq1, seq2, match, mismatch, gap
