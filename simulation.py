import heapq
from typing import Dict, Tuple, Optional

# Constants
TRAVEL_SPEED_FACTOR = 0.5  # Time per unit distance

class Car:
    def __init__(self, car_id, location):
        self.id = car_id
        self.location = location
        self.route = []
        self.route_time = 0
        
        self.status = "available"  # available, en_route_to_pickup, en_route_to_destination
        self.assigned_rider = None
    
    def calculate_route(self, destination, graph=None):
        if graph:
            # Placeholder for future advanced pathfinding
            pass
        else:
            distance = abs(self.location[0] - destination[0]) + abs(self.location[1] - destination[1])
            self.route_time = distance * TRAVEL_SPEED_FACTOR
            self.route = [self.location, destination]
    
    def __str__(self):
        return f"Car {self.id} at {self.location} - Status: {self.status}"

class Rider:
    def __init__(self, rider_id, start_location, destination):
        self.id = rider_id
        self.start_location = start_location
        self.destination = destination
        self.status = "waiting"  # waiting, in_car, completed
    
    def __str__(self):
        return (f"Rider {self.id} at {self.start_location} "
                f"going to {self.destination} - Status: {self.status}")

class Simulation:
    def __init__(self):
        self.current_time = 0
        self.event_heap = []  # Min-heap for events: (timestamp, counter, event_type, data)
        self.cars: Dict[int, Car] = {}
        self.riders: Dict[int, Rider] = {}
        self.event_counter = 0
        self.graph = None
    
    def add_car(self, car: Car):
        self.cars[car.id] = car
    
    def add_rider(self, rider: Rider, request_time: float):
        self.riders[rider.id] = rider
        self.schedule_event(request_time, "RIDER_REQUEST", rider)
    
    def schedule_event(self, timestamp: float, event_type: str, data):
        heapq.heappush(self.event_heap, (timestamp, self.event_counter, event_type, data))
        self.event_counter += 1
    
    def calculate_travel_time(self, start_location: Tuple[float, float], end_location: Tuple[float, float]) -> float:
        distance = abs(start_location[0] - end_location[0]) + abs(start_location[1] - end_location[1])
        return distance * TRAVEL_SPEED_FACTOR
    
    def find_closest_car_brute_force(self, rider_location: Tuple[float, float]) -> Optional[Car]:
        available_cars = [car for car in self.cars.values() if car.status == "available"]
        if not available_cars:
            return None
        
        closest_car = None
        min_distance = float('inf')
        for car in available_cars:
            distance = abs(car.location[0] - rider_location[0]) + abs(car.location[1] - rider_location[1])
            if distance < min_distance:
                min_distance = distance
                closest_car = car
        return closest_car
    
    def handle_rider_request(self, rider: Rider):
        print(f"TIME {self.current_time:.2f}: RIDER {rider.id} requests ride from {rider.start_location} to {rider.destination}")
        
        car = self.find_closest_car_brute_force(rider.start_location)
        
        if car is None:
            print(f"TIME {self.current_time:.2f}: No available cars for RIDER {rider.id}")
            return
        
        car.assigned_rider = rider
        car.status = "en_route_to_pickup"
        
        # Calculate pickup route and time
        car.calculate_route(rider.start_location, self.graph)
        pickup_time = self.current_time + car.route_time
        
        self.schedule_event(pickup_time, "ARRIVAL", car)
        
        print(f"TIME {self.current_time:.2f}: CAR {car.id} dispatched to RIDER {rider.id}")
        print(f"TIME {self.current_time:.2f}: CAR {car.id} will arrive for pickup at TIME {pickup_time:.2f}")
    
    def handle_arrival(self, car: Car):
        if car.status == "en_route_to_pickup":
            rider = car.assigned_rider
            
            print(f"TIME {self.current_time:.2f}: CAR {car.id} picked up RIDER {rider.id}")
            
            car.location = rider.start_location
            car.status = "en_route_to_destination"
            rider.status = "in_car"
            
            # Calculate dropoff route and time
            car.calculate_route(rider.destination, self.graph)
            dropoff_time = self.current_time + car.route_time
            
            self.schedule_event(dropoff_time, "ARRIVAL", car)
            
            print(f"TIME {self.current_time:.2f}: CAR {car.id} heading to destination, will arrive at TIME {dropoff_time:.2f}")
        
        elif car.status == "en_route_to_destination":
            rider = car.assigned_rider
            
            print(f"TIME {self.current_time:.2f}: CAR {car.id} dropped off RIDER {rider.id}")
            
            car.location = rider.destination
            car.status = "available"
            rider.status = "completed"
            
            car.route = []
            car.route_time = 0
            
            car.assigned_rider = None
    
    def run(self, max_time: float = 100.0):
        print("=" * 60)
        print("RIDE-SHARING SIMULATION ENGINE PROTOTYPE")
        print("=" * 60)
        
        while self.event_heap and self.current_time < max_time:
            timestamp, counter, event_type, data = heapq.heappop(self.event_heap)
            self.current_time = timestamp
            
            if event_type == "RIDER_REQUEST":
                self.handle_rider_request(data)
            elif event_type == "ARRIVAL":
                self.handle_arrival(data)
            else:
                print(f"TIME {self.current_time:.2f}: Unknown event type: {event_type}")
            
            print()
        
        print("=" * 60)
        print("SIMULATION COMPLETED")
        print("=" * 60)
        self.print_final_status()
    
    def print_final_status(self):
        print("\nFINAL STATUS:")
        print("-" * 40)
        print("CARS:")
        for car in self.cars.values():
            print(f"  {car}")
        
        print("\nRIDERS:")
        for rider in self.riders.values():
            print(f"  {rider}")

def main():
    sim = Simulation()
    
    car1 = Car(1, (0, 0))
    sim.add_car(car1)
    
    rider1 = Rider(1, (10, 10), (15, 15))
    sim.add_rider(rider1, 1.0)  # Rider 1 requests ride at time 1
    
    # Simulate no cars available by removing all cars before rider 2 requests
    sim.cars = {}  # no cars available
    
    rider2 = Rider(2, (1, 1), (5, 5))
    sim.add_rider(rider2, 2.0)  # Rider 2 requests ride at time 2, no cars available
    
    # Add car back for rider 3
    sim.add_car(car1)
    
    rider3 = Rider(3, (2, 2), (6, 6))
    sim.add_rider(rider3, 3.0)
    
    sim.run(max_time=30.0)

if __name__ == "__main__":
    main()
