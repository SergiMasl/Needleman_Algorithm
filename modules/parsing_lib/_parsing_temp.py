def parsing_2_seq(x, y, pad=1):
    """
    Print a bordered table with `x` as column headers (top) and `y` as row headers (left).
    Cells are empty (no body fill).

    - x: iterable of column header values (top).
    - y: iterable of row header values (left).
    - pad: spaces padding inside each cell.
    """
    xs = [str(v) for v in x]
    ys = [str(v) for v in y]

    col_widths = [max(1, len(h)) for h in xs]
    row_header_width = max((len(s) for s in ys), default=0)

    def hor(w):
        return '-' * (w + pad * 2)

    parts = [hor(row_header_width)] + [hor(w) for w in col_widths]
    top_border = '+' + '+'.join(parts) + '+'

    def cell_content(text, width):
        return ' ' * pad + (text or '').center(width) + ' ' * pad

    header_cells = [cell_content('', row_header_width)] + [cell_content(xs[i], col_widths[i]) for i in range(len(xs))]
    header_line = '|' + '|'.join(header_cells) + '|'

    sep = top_border

    rows = []
    for yi in ys:
        row_header_cell = ' ' * pad + yi.ljust(row_header_width) + ' ' * pad
        empty_cells = [cell_content('', w) for w in col_widths]
        row_line = '|' + '|'.join([row_header_cell] + empty_cells) + '|'
        rows.append(row_line)

    print(top_border)
    if xs or row_header_width:
        print(header_line)
        print(sep)
    for r in rows:
        print(r)
        print(sep)

parsing_2_seq(['A','B'], ['A','B'])