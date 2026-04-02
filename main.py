#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import argparse
import shutil
from pathlib import Path
from modules.input_lib.input import input_sequences
from modules.parsing_lib.get_scoring_parameters import get_scoring_parameters
from modules.parsing_lib.parsing import parsing
from modules.report_lib.report import report, default_report_name
#Updated (3/19/2026)

#make an argument parser to define some CLI options, such as the minimum and
#maximum lengths of sequence inputs. Make CLI options for the match, mismatch,
# and gap penalties 

#MAKE SURE TO IMPORT ALL OTHER LIBRARY MODULES AND NECESSARY EXTENSION MODULES 

#3/19/2026 Added CLI and a class to the main function. Main() will be constructed by
#all team members and making sure all inputs are passed correctly
class CreateAlignment: 

	@staticmethod
	def create_parser() -> argparse.ArgumentParser:
		
		parser = argparse.ArgumentParser(description="Needleman-Wunsch CLI") 
		parser.add_argument( 
			"-i", 
			"--firstseq", 
			type=str ,
			help="Input Sequence #1", 
			)

		parser.add_argument( 
			"-j", 
			"--secondseq", 
			type=str ,
			help="Input Sequence #2", 
			)

		parser.add_argument( 
			"-f", 
			"--inputfasta",
			default = "sequences.fasta", 
			type=str,
			help="Input Fasta File", 
			)

		parser.add_argument( 
			"-m", 
			"--match", 
			type=int,
			default=2,
			help="Input Fasta File", 
			)

		parser.add_argument( 
			"-n", 
			"--mismatch", 
			type=int,
			default=-1,
			help="Input Fasta File", 
			)

		parser.add_argument( 
			"-g", 
			"--gapscore", 
			type=int,
			default=-2,
			help="Input Fasta File", 
			)

		parser.add_argument(
			"-o",
			"--outputfasta",
			type=str,
			default="nwalignment.fasta",
			help="Output Fasta File",
			)

		return parser


	@staticmethod
	def main() -> None:
		parser = CreateAlignment.create_parser()
		args = parser.parse_args()
		file_from_input = input_sequences(args)
		match_score, mismatch_score, gap_penalty = get_scoring_parameters()
		matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty = parsing(file_from_input, match_score, mismatch_score, gap_penalty)

		default_name = default_report_name()
		choice = input("Use default report name (time-based) or enter your own? (default/custom): ").strip().lower()
		while choice not in ("default", "custom"):
			choice = input("Invalid input. Please enter 'default' or 'custom': ").strip().lower()

		if choice == "custom":
			report_name = input("Enter report name: ").strip()
			if not report_name:
				report_name = default_name
		else:
			report_name = default_name

		if not report_name.endswith(".pdf"):
			report_name += ".pdf"

		reports_dir = Path(__file__).parent / "__Reports"
		reports_dir.mkdir(exist_ok=True)
		output_path = str(reports_dir / report_name)

		report(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty, output_path=output_path)



if __name__ == "__main__":
	CreateAlignment.main()
	for cache_dir in Path(__file__).parent.rglob("__pycache__"):
		shutil.rmtree(cache_dir)
