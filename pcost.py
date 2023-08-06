with open(r"Data/portfolio.dat", "r") as f:
    total_price = 0
    for line in f.readlines():
        stock, quantity, value = line.split()
        total_price += float(quantity) * float(value)

print(total_price)
