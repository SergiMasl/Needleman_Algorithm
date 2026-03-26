#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import argparse
from modules.input_lib.input import input_sequences
from modules.parsing_lib.get_scoring_parameters import get_scoring_parameters
from modules.parsing_lib.parsing import parsing
from modules.report_lib.report import report
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
		report(matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty)



if __name__ == "__main__":
	CreateAlignment.main()
