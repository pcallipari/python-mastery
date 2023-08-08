# readrides.py

import csv
import collections.abc
from sys import intern


class RideData(collections.abc.Sequence):
    def __init__(self):
        # Each value is a list with all of the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return {
                "route": self.routes[index],
                "date": self.dates[index],
                "daytype": self.daytypes[index],
                "rides": self.numrides[index],
            }
        elif isinstance(index, slice):
            return_data = RideData()
            if index.step is None:
                indices = range(index.start, index.stop)
            else:
                indices = range(index.start, index.stop, index.step)
            for i in indices:
                return_data.append(self[i])
            return return_data
        else:
            raise TypeError

    def append(self, d):
        self.routes.append(intern(d["route"]))
        self.dates.append(intern(d["date"]))
        self.daytypes.append(intern(d["daytype"]))
        self.numrides.append(d["rides"])


class Row:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_tuples(filename):
    """
    Read the bus ride data as a list of tuples
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            # record = (route, date, daytype, rides)
            record = [route, date, daytype, rides]
            # record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            # record = Row(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of tuples
    """

    records = RideData()
    # records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            # record = (route, date, daytype, rides)
            # record = [route, date, daytype, rides]
            record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            # record = Row(route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_columns(filename):
    """Read the bus ride data into 4 lists, representing columns."""
    routes = []
    dates = []
    daytypes = []
    numrides = []

    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(row[3])
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


class DataCollection(collections.abc.Sequence):
    def __init__(self, headers, types):
        self.types = types
        self.headers = headers
        self.data = {key: [] for key in headers}
        # print()

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.data.items[0])

    def __getitem__(self, index):
        if isinstance(index, int):
            return {name: self.data[name][index] for name in self.headers}
        elif isinstance(index, slice):
            return_data = DataCollection(self.headers, self.types)
            if index.step is None:
                indices = range(index.start, index.stop)
            else:
                indices = range(index.start, index.stop, index.step)
            for i in indices:
                return_data.append(self[i])
            return return_data
        else:
            raise TypeError

    def append(self, d):
        for key, func in zip(d.keys(), self.types):
            self.data[key].append(func(d[key]))


def read_csv_as_columns(filename, types):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        output_data = DataCollection(headers, types)
        for row in rows:
            vals = [func(val) for func, val in zip(types, row)]
            output_data.append({name: val for name, val in zip(headers, vals)})
    return output_data


if __name__ == "__main__":
    import tracemalloc

    # tracemalloc.start()
    # rows = read_rides_as_dicts("Data/ctabus.csv")
    # print("Memory Use: Current %d, Peak %d" % tracemalloc.get_traced_memory())
    # r = rows[0:10]
    # records = RideData()

    data = read_csv_as_columns("Data/ctabus.csv", types=[str, str, str, int])
    print(data)
    print(data[0])
