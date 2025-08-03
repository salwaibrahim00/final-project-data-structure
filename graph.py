import csv

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start, end, weight):
        if start not in self.adjacency_list:
            self.adjacency_list[start] = []
        if end not in self.adjacency_list:
            self.adjacency_list[end] = []
        self.adjacency_list[start].append((end, weight))
        # Uncomment if graph is undirected (two-way streets)
        # self.adjacency_list[end].append((start, weight))

    def load_from_file(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 3:
                    start, end, weight = row[0], row[1], int(row[2])
                    self.add_edge(start, end, weight)

    def __str__(self):
        result = ""
        for node, neighbors in self.adjacency_list.items():
            result += f"{node}: {neighbors}\n"
        return result
