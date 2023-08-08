import csv


class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = int(shares)
        self.price = float(price)

    def cost(self):
        return self.shares * self.price

    def sell(self, amount):
        self.shares -= amount


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
