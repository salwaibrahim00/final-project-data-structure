from graph import Graph
from car import Car

# load up the map
graph = Graph()
graph.load_from_file("map.csv")

# make a car starting at point A
car1 = Car("C1", "A")

# figure out how to get to D
car1.calculate_route("D", graph)

# show what we got
print(f"Car route: {car1.route}")
print(f"Travel time: {car1.route_time}")
