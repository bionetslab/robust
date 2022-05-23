def read_terminals(path: str):
    seeds = []
    with open(path) as file:
        for line in file:
            seeds.append(line.strip())
    return seeds