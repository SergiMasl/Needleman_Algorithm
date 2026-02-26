
"""
validation.py

Validate DNA sequences and scoring parameters before running
the Needleman–Wunsch alignment algorithm.

- Cleans sequences (remove whitespace, convert to uppercase)
- Ensures sequences contain only A, C, G, T
- Validates scoring values (match, mismatch, gap)
"""


# Allowed DNA characters
VALID_DNA = {"A", "C", "G", "T"}


def normalize_sequence(seq):
    """
    Clean a DNA sequence by removing whitespace and converting to uppercase.
    """
    if seq is None:
        return ""
    return "".join(seq.split()).upper()


def validate_dna_sequence(seq, name="sequence"):
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


def validate_int(value, name):
    """
    Validate that a value can be converted to an integer.
    """
    try:
        return int(value)
    except:
        raise ValueError(f"{name} must be an integer. You entered: {value}")


def validate_scoring(match, mismatch, gap):
    """
    Validate scoring configuration before alignment.
    Returns (match, mismatch, gap) if valid.
    """
    if match == 0 and mismatch == 0 and gap == 0:
        raise ValueError(
            "Scoring cannot be all zeros; alignment would be meaningless."
        )

    return match, mismatch, gap



# Mehrnoush will be doing the validation function(s)
