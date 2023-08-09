def print_table(data: list, headers: list):
    print("".join("{:>10}".format(i) for i in headers))
    print("-" * 10 * len(headers))
    for obj in data:
        current_strings = []
        for attr in headers:
            val = getattr(obj, attr)
            if isinstance(val, float):
                current_strings.append("{:>10.2f}".format(val))
            else:
                current_strings.append("{:>10}".format(val))
        print("".join(current_strings))
