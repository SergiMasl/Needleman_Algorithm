import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def report(matrix: np.ndarray, seq_a: str, seq_b: str,
           match: int, mismatch: int, gap: int,
           output_path: str = "nw_report.pdf") -> str:
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

    Returns: output_path
    """
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

    fig.suptitle(
        f"Needleman-Wunsch Scoring Matrix\n"
        f"match={match}  mismatch={mismatch}  gap={gap}",
        fontsize=11
    )

    with PdfPages(output_path) as pdf:
        pdf.savefig(fig, bbox_inches="tight")

    plt.close(fig)
    print(f"Report saved to: {output_path}")
    return output_path
