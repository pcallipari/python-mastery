from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplemented

    @abstractmethod
    def row(self, rowdata):
        raise NotImplemented


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % item) for fmt, item in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


class TextTableFormatter(TableFormatter, ColumnFormatMixin, UpperHeadersMixin):
    def headings(self, headers):
        print(" ".join("{:>10}".format(h) for h in headers))
        print(("-" * 10) * len(headers))

    def row(self, rowdata):
        print(" ".join("{:>10}".format(d) for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(str(r) for r in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print(
            "<tr> ", "".join("<th>{}</th> ".format(name) for name in headers), "</tr>"
        )

    def row(self, rowdata):
        print("<tr> ", "".join("<td>{}</td> ".format(r) for r in rowdata), "</tr>")


def create_formatter(formatter_name, column_formats=None, upper_headers=False):
    if formatter_name == "text":
        formatter_cls = TextTableFormatter
    elif formatter_name == "csv":
        formatter_cls = CSVTableFormatter
    elif formatter_name == "html":
        formatter_cls = HTMLTableFormatter
    else:
        raise ValueError("Invalid formatter name")

    if column_formats:

        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats

    if upper_headers:

        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()


def print_table(records: list, headers: list, formatter: TableFormatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(headers)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in headers]
        formatter.row(rowdata)
