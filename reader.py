import csv


def read_csv_as_dicts(filename, typefuncs):
    output_list = []
    with open(filename, "r") as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            output_list.append(
                {name: func(val) for name, func, val in zip(headers, typefuncs, row)}
            )
    return output_list


def read_csv_as_instances(filename, cls):
    """
    Read a CSV file into a list of instances
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records
