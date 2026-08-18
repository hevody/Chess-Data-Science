from tabulate import tabulate

data = [
    ["1. d4 d5 2. c4", "2", "c4"],
    ["Bob", "Manager", "London"],
    ["Charlie", "Designer", "Tokyo"]
]
headers = ["Line", "Frequency", "Mainline Move"]

# Generate a clean, makeshift terminal grid
print(tabulate(data, headers=headers, tablefmt="grid"))
