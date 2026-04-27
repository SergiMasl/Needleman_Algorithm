#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
from datetime import datetime
from typing import Tuple


def default_report_name() -> str:
	return datetime.now().strftime("%Y-%m-%d_%H-%M-%S.pdf")


def _gc_content(seq: str) -> float:
	"""Return GC content as a percentage (0-100) for a DNA sequence."""
	seq = seq.upper()
	gc = sum(1 for base in seq if base in ("G", "C"))
	return (gc / len(seq) * 100) if seq else 0.0


def traceback_graphing(matrix: np.ndarray, seq_a: str, seq_b: str,
					 match: int, mismatch: int, gap: int, tie_point: Tuple = None) -> set:
	path = set()
	i, j = tie_point if tie_point else (matrix.shape[0] - 1, matrix.shape[1] - 1)
	path.add((matrix.shape[0] - 1, matrix.shape[1] - 1)) #makes sure the bottom right cell remains

	if tie_point:
		score = match if seq_b[i-1].upper() == seq_a[j-1].upper() else mismatch
		diag  = matrix[i-1][j-1] + score
		up    = matrix[i-1][j] + gap
		left  = matrix[i][j-1] + gap
		current = matrix[i][j]
		path.add((i, j))

		if current == diag and current == up:
			i -= 1  # take up instead of diag
		elif current == diag and current == left:
			j -= 1  # take left instead of diag
		else:
			j -= 1  # take left instead of up
 
	while i > 0 or j > 0:
		path.add((i, j))
 
		if i == 0:
			j -= 1
		elif j == 0:
			i -= 1
		else:
			score = match if seq_b[i - 1].upper() == seq_a[j - 1].upper() else mismatch
			diag  = matrix[i - 1][j - 1] + score
			up    = matrix[i - 1][j] + gap
			left  = matrix[i][j - 1] + gap
 
			current = matrix[i][j]
			if current == diag:
				i -= 1
				j -= 1
			elif current == up:
				i -= 1
			else:
				j -= 1
 
	path.add((0, 0))  # include the origin cell
	return path


def report(matrix: np.ndarray, seq_a: str, seq_b: str,
		   match: int, mismatch: int, gap: int,
		   output_path: str = None, tie_point: Tuple = None) -> str:
	"""
	Purpose: Generate a PDF report of the Needleman-Wunsch scoring matrix.

	Parameters:
		matrix      - completed NW scoring matrix from parsing()
		seq_a       - sequence across columns
		seq_b       - sequence down rows
		match       - match score used
		mismatch    - mismatch score used
		gap         - gap penalty used
		output_path - file path for the output PDF
		tie_point   - optional tuple for alt. traceback path

	Returns: output_path
	"""
	if output_path is None:
		reports_dir = Path(__file__).parents[2] / "__Reports"
		reports_dir.mkdir(exist_ok=True)
		output_path = str(reports_dir / default_report_name())

	# Traceback: find which cells are on the optimal alignment path 
	path_cells = traceback_graphing(matrix, seq_a, seq_b, match, mismatch, gap)

	col_labels = [" "] + list(seq_a)
	row_labels = [" "] + list(seq_b)
	cell_text = [[str(matrix[i][j]) for j in range(matrix.shape[1])]
				 for i in range(matrix.shape[0])]

	fig, ax = plt.subplots(figsize=(max(8, len(seq_a) * 0.6),
									max(4, len(seq_b) * 0.4)))
	ax.axis("off")

	table = ax.table(
		cellText=cell_text,
		rowLabels=row_labels,
		colLabels=col_labels,
		loc="center",
		cellLoc="center"
	)
	table.auto_set_font_size(False)
	table.set_fontsize(9)
	table.scale(1, 1.4)

	# Highlight the traceback's path cells                                 
	highlight_col  = "#B3B3B3"   # light grey fill
	highlight_edge   = "#4A4A4A"   # darker outer border for highlighting
	default_edge     = "#4A4A4A" # All edges are the same color as the highlight edge
 
	for (i, j), cell in table.get_celld().items():
		# i==0 → column-header row; j==-1 → row-label column
		if i == 0 or j == -1:
			cell.set_edgecolor(default_edge)
			continue
		data_row = i - 1 # convert table row → matrix row
		data_col = j # table col == matrix col (no offset needed)
		if (data_row, data_col) in path_cells:
			cell.set_facecolor(highlight_col)
			cell.set_edgecolor(highlight_edge)
			cell.set_text_props(fontweight="bold")
		else:
			cell.set_edgecolor(default_edge)

	fig.suptitle(
		f"Needleman-Wunsch Scoring Matrix\n"
		f"match={match} mismatch={mismatch} gap={gap}",
		fontsize=11
	)

	# Sequence stats
	gc_a = _gc_content(seq_a)
	gc_b = _gc_content(seq_b)

	stats_labels = ["Metric", "Sequence A", "Sequence B"]
	stats_data = [
		["Base pairs", str(len(seq_a)), str(len(seq_b))],
		["GC content (%)", f"{gc_a:.1f}", f"{gc_b:.1f}"],
	]

	fig2, ax2 = plt.subplots(figsize=(6, 2))
	ax2.axis("off")
	stats_table = ax2.table(
		cellText=stats_data,
		colLabels=stats_labels,
		loc="center",
		cellLoc="center"
	)
	stats_table.auto_set_font_size(False)
	stats_table.set_fontsize(10)
	stats_table.scale(1, 1.8)
	fig2.suptitle("Sequence Statistics", fontsize=12, fontweight="bold")

	if tie_point:
		alt_path_cells = traceback_graphing(matrix, seq_a, seq_b, match, mismatch, gap, tie_point)

		fig3, ax3 = plt.subplots(figsize=(max(8, len(seq_a) * 0.6),
										  max(4, len(seq_b) * 0.4)))
		ax3.axis("off")

		table3 = ax3.table(
			cellText=cell_text,
			rowLabels=row_labels,
			colLabels=col_labels,
			loc="center",
			cellLoc="center"
		)
		table3.auto_set_font_size(False)
		table3.set_fontsize(9)
		table3.scale(1, 1.4)

		for (i, j), cell in table3.get_celld().items():
			if i == 0 or j == -1:
				cell.set_edgecolor(default_edge)
				continue
			data_row = i - 1
			data_col = j
			if (data_row, data_col) in alt_path_cells:
				cell.set_facecolor(highlight_col)
				cell.set_edgecolor(highlight_edge)
				cell.set_text_props(fontweight="bold")
			else:
				cell.set_edgecolor(default_edge)

		fig3.suptitle(
			f"Needleman-Wunsch Alternate Traceback\n"
			f"match={match} mismatch={mismatch} gap={gap}",
			fontsize=11
		)

		with PdfPages(output_path) as pdf:
			pdf.savefig(fig, bbox_inches="tight")
			pdf.savefig(fig2, bbox_inches="tight")
			pdf.savefig(fig3, bbox_inches="tight")

		plt.close(fig3)

	else:
		with PdfPages(output_path) as pdf:
			pdf.savefig(fig, bbox_inches="tight")
			pdf.savefig(fig2, bbox_inches="tight")

	plt.close(fig)
	plt.close(fig2)
	print(f"Report saved to: {output_path}")
	return output_path

