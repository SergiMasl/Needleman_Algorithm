#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py

Main execution file for the Needleman-Wunsch alignment project.

Purpose:
- Acts as the central controller of the program
- Handles command-line user input
- Passes data between project modules
- Runs alignment and generates final report

Run Example:
python main.py -i ACGT -j AGGT -m 2 -n -1 -g -2 -o report.pdf
"""

import argparse
import shutil
from pathlib import Path

from modules.input_lib.input import input_sequences
from modules.parsing_lib.parsing import parsing
from modules.report_lib.report import report, default_report_name


# Updated by: Mehrnoush Fereydouni
# Last Updated: April 23, 2026
# Changes:
# - Removed interactive scoring input from main.py
# - Removed interactive report name prompt
# - Updated CLI help messages
# - Renamed --outputfasta to --outputpdf
# - Kept PDF output in the __Reports directory


class CreateAlignment:
	"""
	Purpose:
		Manage the overall execution flow of the program.

	Functions:
		create_parser() -> Builds command-line interface
		main() -> Runs complete alignment workflow
	"""

	@staticmethod
	def create_parser() -> argparse.ArgumentParser:
		"""
		Purpose:
			Create command-line arguments for the program.

		Returns:
			Configured argparse parser object.
		"""
		parser = argparse.ArgumentParser(
			description="Needleman-Wunsch global alignment CLI"
		)

		parser.add_argument(
			"-i",
			"--firstseq",
			type=str,
			help="First input DNA sequence",
		)

		parser.add_argument(
			"-j",
			"--secondseq",
			type=str,
			help="Second input DNA sequence",
		)

		parser.add_argument(
			"-f",
			"--inputfasta",
			type=str,
			default="sequences.fasta",
			help="Input FASTA file containing sequences",
		)

		parser.add_argument(
			"-m",
			"--match",
			type=int,
			default=None,
			help="Match score (default 2; omit to be prompted)",
		)

		parser.add_argument(
			"-n",
			"--mismatch",
			type=int,
			default=None,
			help="Mismatch penalty (default -1; omit to be prompted)",
		)

		parser.add_argument(
			"-g",
			"--gapscore",
			type=int,
			default=None,
			help="Gap penalty (default -2; omit to be prompted)",
		)

		parser.add_argument(
			"-o",
			"--outputpdf",
			type=str,
			default=default_report_name(),
			help="Output PDF report filename",
		)

		return parser

	@staticmethod
	def main() -> None:
		"""
		Purpose:
			Run the complete program workflow.

		Steps:
		1. Read command-line arguments
		2. Collect sequence input
		3. Retrieve scoring values
		4. Run Needleman-Wunsch parsing
		5. Generate final PDF report
		"""
		parser = CreateAlignment.create_parser()
		args = parser.parse_args()

		# Retrieve sequence input
		file_from_input = input_sequences(args)

		# Retrieve scoring values
		match_score = args.match
		mismatch_score = args.mismatch
		gap_penalty = args.gapscore

		# Run alignment algorithm
		matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty, tie_point = parsing(
			file_from_input,
			match_score,
			mismatch_score,
			gap_penalty,
		)

		# Output report name
		report_name = args.outputpdf
		if not report_name.endswith(".pdf"):
			report_name += ".pdf"

		# Create reports folder if missing
		reports_dir = Path(__file__).parent / "__Reports"
		reports_dir.mkdir(exist_ok=True)

		output_path = str(reports_dir / report_name)

		# Generate final report
		report(
			matrix,
			seq_a,
			seq_b,
			match_score,
			mismatch_score,
			gap_penalty,
			tie_point=tie_point,
			output_path=output_path,
		)

# Guard Function
if __name__ == "__main__":
	try:
		CreateAlignment.main()
	except (ValueError, TypeError, AttributeError, IndexError, OSError, RuntimeError) as e:
		print(f"Error: {e}")
		raise SystemExit(1)
	except Exception as e:
		print(f"Unexpected error: {e}")
		raise SystemExit(1)
	finally:
		# Remove temporary cache folders whether the run succeeded or failed
		for cache_dir in Path(__file__).parent.rglob("__pycache__"):
			shutil.rmtree(cache_dir)
