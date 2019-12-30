class MarkDownWriter:
    def __init__(self, filename: str, mode="w"):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.markdown_file = open(self.filename, self.mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.markdown_file.close()

    def header_1(self, header: str):
        """Add H1 header"""
        self.markdown_file.write(f"# {header}\n")

    def header_2(self, header: str):
        """Add H2 header"""
        self.markdown_file.write(f"## {header}\n")

    def header_3(self, header: str):
        """Add H3 header"""
        self.markdown_file.write(f"## {header}\n")

    def add_line(self, text: str):
        """Add line of text"""
        self.markdown_file.write(f"{text}  \n")

    def newline(self):
        """Add new line character"""
        self.markdown_file.write("\n")

    def separator(self):
        """Add separator, aka horizontal rule"""
        self.markdown_file.write("---\n")

    def table(self, columns: list, data: list):
        """Add a table

        :param columns: list of tuples: (column name, width, alignment)
        :param data: list of tuples: (values for one row)
        """
        self._add_table_header_or_row([(column[0], column[1]) for column in columns])
        self._add_table_header_separator([(column[2], column[1]) for column in columns])
        for row in data:
            self._add_table_header_or_row(zip(row, [column[1] for column in columns]))
        self.newline()

    def _add_table_header_or_row(self, row_items: iter):
        """Create a table header or a data row

        :param row_items: iterator of tuples: (data value, column width)
        """
        data_items = [f"{item[0]:{item[1]}}" for item in row_items]
        row = "| " + " | ".join(data_items) + " |\n"
        self.markdown_file.write(row)

    def _add_table_header_separator(self, separator_items: iter):
        """Create a table header separator row

        :param separator_items: iterator of tuples: (alignment, column width)"""
        separator = ["|"]
        for item in separator_items:
            if item[0] in ("left", "L"):
                separator.append(f"{' :' + '-'*(item[1]-1) + ' |'}")
            if item[0] in ("center", "C"):
                separator.append(f"{' :' + '-'*(item[1]-2) + ': |'}")
            elif item[0] in ("right", "R"):
                separator.append(f"{' ' + '-'*(item[1]-1) + ': |'}")
        separator.append("\n")
        self.markdown_file.write("".join(separator))
