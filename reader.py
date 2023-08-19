import csv
from abc import ABC, abstractmethod


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types) -> None:
        self.types = types

    def make_record(self, headers, row):
        return {name: func(val) for name, func, val in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls) -> None:
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_dicts(filename, typefuncs):
    parser = DictCSVParser(typefuncs)
    return parser.parse(filename)
    # output_list = []
    # with open(filename, "r") as f:
    #     rows = csv.reader(f)
    #     headers = next(rows)
    #     for row in rows:
    #         output_list.append(
    #             {name: func(val) for name, func, val in zip(headers, typefuncs, row)}
    #         )
    # return output_list


def read_csv_as_instances(filename, cls):
    """
    Read a CSV file into a list of instances
    """
    return InstanceCSVParser(cls).parse(filename)
    # records = []
    # with open(filename) as f:
    #     rows = csv.reader(f)
    #     headers = next(rows)
    #     for row in rows:
    #         records.append(cls.from_row(row))
    # return records
