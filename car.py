from pathfinding import find_shortest_path

class Car:
    def __init__(self, car_id, location):
        # car's ID
        self.id = car_id
        # where the car is right now
        self.location = location
        # empty route to start
        self.route = []
        # how long the route takes
        self.route_time = 0
    
    def calculate_route(self, destination, graph):
        # get shortest path to destination
        path, travel_time = find_shortest_path(graph, self.location, destination)
        # save the path
        self.route = path
        # save how long it takes
        self.route_time = travel_time
