import csv
from decimal import Decimal


class Stock:
    _types = (str, int, float)
    __slots__ = ("_name", "_shares", "_price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, self._types[0]):
            raise TypeError
        self._name = value

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError
        elif value < 0:
            raise ValueError
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError
        elif value < 0.0:
            raise ValueError
        self._price = value

    def __repr__(self) -> str:
        return "Stock({},{},{})".format(self.name, self.shares, self.price)

    def __eq__(self, other) -> bool:
        if isinstance(other, Stock):
            if (self.name, self.shares, self.price) == (
                other.name,
                other.shares,
                other.price,
            ):
                return True
        return False

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, amount):
        self.shares -= amount

    @classmethod
    def from_row(cls, row):
        vals = [func(val) for func, val in zip(cls._types, row)]
        return cls(*vals)


class DStock(Stock):
    _types = (str, int, Decimal)


import sys


class redirect_stdout:
    def __init__(self, out_file):
        self.out_file = out_file

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout


def read_portfolio(filename: str):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        portfolio = []
        for name, shares, price in rows:
            portfolio.append(Stock(name, shares, price))
        return portfolio


def print_portfolio(portfolio):
    print("%10s %10s %10s" % ("name", "shares", "price"))
    for stock in portfolio:
        print("%10s %10d %10.2f" % (stock.name, stock.shares, stock.price))
