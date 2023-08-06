# with open(r"Data/portfolio3.dat", "r") as f:
#     total_price = 0
#     for line in f.readlines():
#         stock, quantity, value = line.split()
#         total_price += float(quantity) * float(value)


def portfolio_cost(input_file: str) -> float:
    with open(input_file, "r") as f:
        total_price = 0
        for line in f.readlines():
            try:
                stock, quantity, value = line.split()
                total_price += int(quantity) * float(value)
            except ValueError as e:
                print(f"Couldn't parse line: '{line}'")
                print(f"Reason: '{e}''")

    return total_price


# print(portfolio_cost(r"Data/portfolio3.dat"))
# print(total_price)

if __name__ == "__main__":
    print(portfolio_cost(r"Data/portfolio.dat"))
