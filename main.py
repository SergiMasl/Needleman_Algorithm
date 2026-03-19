#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import argparse 
from 
#Updated (3/19/2026)

#make an argument parser to define some CLI options, such as the minimum and
#maximum lengths of sequence inputs. Make CLI options for the match, mismatch,
# and gap penalties 

#MAKE SURE TO IMPORT ALL OTHER LIBRARY MODULES AND NECESSARY EXTENSION MODULES 

#3/19/2026 Added CLI and a class to the main function. Main() will be constructed by
#all team members and making sure all inputs are passed correctly
class CreateAlignment: 

	def __init__(
		self, 
		input_file: str= None,
		sequence1: str= None, 
		sequence2: str= None,
		match:int = 2, 
		mismatch:int = -1, 
		gap:int = -2
		) -> None 

	def create_parser() -> argparse.ArgumentParser: 

		#Setting the scoring scheme to a default (modify as a last improvement):
		#Match = +2
		#Mismatch = -1
		#Gap Penalty = -2

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


	def main() -> None 



if __name__ == "__main__":
	main()
