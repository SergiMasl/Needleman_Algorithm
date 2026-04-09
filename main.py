#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import shutil
from pathlib import Path
from modules.input_lib.input import input_sequences
from modules.parsing_lib.parsing import parsing
from modules.report_lib.report import report, default_report_name

# Updated: April 9, 2026
# - Removed interactive scoring input from main.py
# - Removed interactive report name prompt
# - Updated CLI help messages
# - Renamed --outputfasta to --outputpdf
# - Kept PDF output in the __Reports directory


class CreateAlignment:
    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
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
            default=2,
            help="Match score",
        )

        parser.add_argument(
            "-n",
            "--mismatch",
            type=int,
            default=-1,
            help="Mismatch penalty",
        )

        parser.add_argument(
            "-g",
            "--gapscore",
            type=int,
            default=-2,
            help="Gap penalty",
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
        parser = CreateAlignment.create_parser()
        args = parser.parse_args()

        file_from_input = input_sequences(args)

        match_score = args.match
        mismatch_score = args.mismatch
        gap_penalty = args.gapscore

        matrix, seq_a, seq_b, match_score, mismatch_score, gap_penalty = parsing(
            file_from_input,
            match_score,
            mismatch_score,
            gap_penalty,
        )

        report_name = args.outputpdf
        if not report_name.endswith(".pdf"):
            report_name += ".pdf"

        reports_dir = Path(__file__).parent / "__Reports"
        reports_dir.mkdir(exist_ok=True)
        output_path = str(reports_dir / report_name)

        report(
            matrix,
            seq_a,
            seq_b,
            match_score,
            mismatch_score,
            gap_penalty,
            output_path=output_path,
        )


if __name__ == "__main__":
    CreateAlignment.main()
    for cache_dir in Path(__file__).parent.rglob("__pycache__"):
        shutil.rmtree(cache_dir)
