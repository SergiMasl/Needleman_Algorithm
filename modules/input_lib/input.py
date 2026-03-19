"""
input.py
Supports FASTA file input and inline sequence strings for Needleman-Wunsch global alignment tool.
Returns False on any error for next module (check_false.py?) to handle. 
"""

import sys 
from dataclasses import dataclass 
from validation import validate_dna_sequence

class SequenceInput:
	"""
	Stores the two DNA sequences and their names. 
	This is what gets passed to main.oy to then move forward.
	"""
	seq_a: str
	seq_b: str 
	label_a: str 
	label_b: str 


	def parse_fasta_file(file: str) -> tuple[str, str]:
		"""
		Opens a FASTA file and reads the DNA sequence inside it. Returns the sequence 
		as a string, or False if something goes wrong. Handles one file at a time by 
		design. 
	
		Args: 

		Returns: 

		Raises: 

		Example: 
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
			sequence = sequence + line.strip()


	def read_two_fastas(file1: str, file2: str) -> tuple[str,str, str, str]:
		""" 
		Reads two FASTA lines and returns both sequences and their 
		labels. Returns false if either file fails.
	
		Args: 

		Returns: 

		Raises: 

		Example: 
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

		Args: 

		Returns: 

		Example:
		"""
		try: 
			seq_a = validate_dna_sequence(raw_a, name=label_a)
			seq_b = validate_dna_sequence(raw_b, name=label_b)
		except ValueError as error: 
			sys.stderr.write(f"[Error] {error}\n")
			return False 
		return SequenceInput(seq_a=seq_a, seq_b=seq_b, label_a=label_a, label_b=label_b)  
