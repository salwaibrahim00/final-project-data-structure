# rider.py
# Enhanced Rider class for discrete-event simulation engine

class Rider:
    def __init__(self, rider_id, start_location, destination):
        """
        Initialize a rider for the ride-sharing simulation.
        
        Args:
            rider_id: Unique identifier for the rider
            start_location: Tuple (x, y) representing pickup location
            destination: Tuple (x, y) representing dropoff location
        """
        self.id = rider_id
        self.start_location = start_location
        self.destination = destination
        self.status = "waiting"  # waiting, in_car, completed
    
    def request_ride(self):
        """Mark that rider has requested a ride"""
        self.status = "waiting"
    
    def get_picked_up(self):
        """Mark that rider has been picked up"""
        self.status = "in_car"
    
    def complete_ride(self):
        """Mark that rider's journey is complete"""
        self.status = "completed"
    
    def is_waiting(self):
        """Check if rider is waiting for pickup"""
        return self.status == "waiting"
    
    def is_in_car(self):
        """Check if rider is currently in a car"""
        return self.status == "in_car"
    
    def is_completed(self):
        """Check if rider's journey is completed"""
        return self.status == "completed"
    
    def calculate_trip_distance(self):
        """Calculate Manhattan distance for the trip"""
        return abs(self.destination[0] - self.start_location[0]) + abs(self.destination[1] - self.start_location[1])
    
    def __str__(self):
        """String representation of the rider"""
        return (f"Rider {self.id}: {self.start_location} → {self.destination} "
                f"[Status: {self.status}]")
    
    def __repr__(self):
        """Technical representation of the rider"""
        return (f"Rider(id={self.id}, start={self.start_location}, "
                f"dest={self.destination}, status='{self.status}')")
