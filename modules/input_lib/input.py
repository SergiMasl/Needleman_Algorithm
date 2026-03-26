"""
input.py
Supports FASTA file input and inline sequence strings for Needleman-Wunsch global alignment tool.
Returns False on any error for next module (check_false.py?) to handle.
"""

import sys
from dataclasses import dataclass
from modules.volidation_lib.validation import validate_dna_sequence


@dataclass
class SequenceInput:
	"""
	Stores the two DNA sequences and their names.
	This is what gets passed to main.py to then move forward.
	"""
	seq_a: str
	seq_b: str
	label_a: str
	label_b: str


def parse_fasta_file(file: str):
	"""
	Opens a FASTA file and reads the first DNA sequence inside it.
	Returns (label, sequence) or False if something goes wrong.
	"""
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

	if lines[0].startswith(">"):
		label = lines[0][1:].strip()
		start = 1

	sequence = ""
	for line in lines[start:]:
		if line.startswith(">"):
			break
		sequence = sequence + line.strip()

	return label, sequence


def read_two_fastas(file1: str, file2: str):
	"""
	Reads two separate FASTA files and returns both sequences and their labels.
	Returns False if either file fails.
	"""
	result_a = parse_fasta_file(file1)
	result_b = parse_fasta_file(file2)

	if result_a is False or result_b is False:
		return False

	label_a, seq_a = result_a
	label_b, seq_b = result_b

	return label_a, seq_a, label_b, seq_b


def build_sequence_input(raw_a: str, raw_b: str, label_a: str, label_b: str):
	"""
	Validates both DNA sequences and packages them into a SequenceInput. Returns False if either
	sequence contains invalid characters.
	"""
	try:
		seq_a = validate_dna_sequence(raw_a, name=label_a)
		seq_b = validate_dna_sequence(raw_b, name=label_b)
	except ValueError as error:
		sys.stderr.write(f"[Error] {error}\n")
		return False
	return SequenceInput(seq_a=seq_a, seq_b=seq_b, label_a=label_a, label_b=label_b)


def input_sequences(args):
	"""
	Asks the user whether to load sequences from a FASTA file or type them manually.
	Returns a SequenceInput object, or exits on error.
	"""
	choice = input("Do you want to load sequences from a FASTA file or type them manually? (fasta/manual): ")
	while choice.lower() not in ["fasta", "manual"]:
		choice = input("Invalid input. Please enter 'fasta' or 'manual': ")

	if choice.lower() == "fasta":
		file_path = input(f"Enter FASTA file path (default: {args.inputfasta}): ").strip()
		if not file_path:
			file_path = args.inputfasta
		parsed = parse_fasta_file(file_path)
		if parsed is False:
			sys.exit(1)
		label_a, seq_a = parsed
		raw_b = input("Enter second DNA sequence: ")
		result = build_sequence_input(seq_a, raw_b, label_a, "seq2")
	else:
		raw_a = input("Enter first DNA sequence: ")
		raw_b = input("Enter second DNA sequence: ")
		result = build_sequence_input(raw_a, raw_b, "seq1", "seq2")

	if result is False:
		sys.exit(1)
	return result
