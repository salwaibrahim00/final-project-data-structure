from graph import Graph

class Simulation:
    def __init__(self, map_filename):
        self.map = Graph()
        self.map.load_from_file(map_filename)
        self.cars = {}  # Optional, for future use
        self.rides = {}  # Optional, for future use

    def display_map(self):
        print(self.map)

if __name__ == "__main__":
    sim = Simulation("map.csv")
    sim.display_map()
