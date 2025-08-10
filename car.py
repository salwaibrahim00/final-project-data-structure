# car.py
# Enhanced Car class for discrete-event simulation engine

# Constants
TRAVEL_SPEED_FACTOR = 0.5  # Time per unit distance (for placeholder navigation)

class Car:
    def __init__(self, car_id, location):
        """
        Initialize a car for the ride-sharing simulation.
        
        Args:
            car_id: Unique identifier for the car
            location: Tuple (x, y) representing car's current position
        """
        self.id = car_id
        self.location = location
        self.route = []
        self.route_time = 0
        
        # Status control
        self.status = "available"  # available, en_route_to_pickup, en_route_to_destination
        self.assigned_rider = None  # Link to rider when dispatched
    
    def calculate_route(self, destination, graph=None):
        """
        Calculate route to destination using pathfinding algorithm.
        
        Args:
            destination: Tuple (x, y) representing target location
            graph: Graph object for pathfinding (None for prototype)
        """
        if graph:
            # For final version with your graph and pathfinding:
            pass
        
        # Placeholder calculation for prototype (Manhattan distance)
        distance = abs(self.location[0] - destination[0]) + abs(self.location[1] - destination[1])
        self.route_time = distance * TRAVEL_SPEED_FACTOR
        self.route = [self.location, destination]
    
    def is_available(self):
        """Check if car is available for assignment"""
        return self.status == "available"
    
    def assign_rider(self, rider):
        """Assign a rider to this car and set status"""
        self.assigned_rider = rider
        self.status = "en_route_to_pickup"
        self.calculate_route(rider.start_location)  # Added: compute pickup route
    
    def complete_pickup(self):
        """Mark that car has completed pickup"""
        if self.assigned_rider:
            self.location = self.assigned_rider.start_location
            self.status = "en_route_to_destination"
            self.calculate_route(self.assigned_rider.destination)  # Added: compute dropoff route
    
    def complete_dropoff(self):
        """Mark that car has completed dropoff"""
        if self.assigned_rider:
            self.location = self.assigned_rider.destination
            self.status = "available"
            self.assigned_rider = None
            self.route = []
            self.route_time = 0
    
    def __str__(self):
        """String representation of the car"""
        rider_info = f" (assigned to Rider {self.assigned_rider.id})" if self.assigned_rider else ""
        return f"Car {self.id} at {self.location} - Status: {self.status}{rider_info}"
    
    def __repr__(self):
        """Technical representation of the car"""
        return f"Car(id={self.id}, location={self.location}, status='{self.status}')"
