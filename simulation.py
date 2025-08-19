import heapq
import random
import argparse
import matplotlib.pyplot as plt  # Standard plotting library
from quadtree import Quadtree, Rectangle
from dijkstra import find_shortest_path
from rider import Rider
from graph import Graph

class Car:
    def __init__(self, car_id, start_position):
        self.car_id = car_id
        self.position = start_position
        self.available = True
        self.rides_completed = 0

    def __repr__(self):
        return f"Car({self.car_id}, pos={self.position}, available={self.available})"


class RideSharingSimulation:
    def __init__(self, max_time=100, mean_arrival_time=5, map_file='map.csv'):
        self.max_time = max_time
        self.mean_arrival_time = mean_arrival_time
        self.current_time = 0
        self.next_rider_id = 1
        
        # Load map and setup quadtree for fast car lookup
        self.graph = Graph()
        self.graph.load_map_data(map_file)
        
        min_x, min_y, max_x, max_y = self.graph.get_bounds()
        boundary = Rectangle(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
        self.quadtree = Quadtree(boundary, capacity=4)
        
        # Simulation state
        self.cars = []
        self.events = []
        self.completed_rides = []
        self.trip_data = []
        self.total_riders_generated = 0

    def add_car(self, car):
        self.cars.append(car)
        self.quadtree.insert(car.position, car)

    def generate_rider_request(self):
        """Generate a rider with random start and end points"""
        min_x, min_y, max_x, max_y = self.graph.get_bounds()
        start_x = random.uniform(min_x, max_x)
        start_y = random.uniform(min_y, max_y)
        end_x = random.uniform(min_x, max_x)
        end_y = random.uniform(min_y, max_y)
        
        rider = Rider(self.next_rider_id, (start_x, start_y), (end_x, end_y))
        self.total_riders_generated += 1
        self.next_rider_id += 1
        return rider

    def run(self):
        # Start with first rider request
        heapq.heappush(self.events, (0, "rider_request", None))

        # Process events until simulation ends
        while self.events and self.current_time < self.max_time:
            time, event_type, data = heapq.heappop(self.events)
            
            if time > self.max_time:
                break
                
            self.current_time = time

            if event_type == "rider_request":
                self.handle_rider_request()
            elif event_type == "pickup_arrival":
                car, rider = data
                self.handle_pickup_arrival(car, rider)
            elif event_type == "ride_complete":
                car, rider = data
                self.handle_ride_complete(car, rider)

    def handle_rider_request(self):
        rider = self.generate_rider_request()
        rider.request_time = self.current_time
        
        # Find nearest available cars and pick the best one
        k_nearest = self.quadtree.find_k_nearest(rider.start_location, k=5)
        
        best_car = None
        best_time = float('inf')
        
        for car_location in k_nearest:
            car = self.quadtree.get_car_at_location(car_location)
            if car and car.available:
                car_node = self.graph.find_nearest_vertex(car.position)
                rider_node = self.graph.find_nearest_vertex(rider.start_location)
                _, travel_time = find_shortest_path(self.graph, car_node, rider_node)
                
                if travel_time < best_time:
                    best_time = travel_time
                    best_car = car
        
        if best_car:
            # Assign car to rider
            self.quadtree.remove(best_car.position)
            best_car.available = False
            
            # Calculate pickup and dropoff times
            pickup_time = self.current_time + best_time
            pickup_node = self.graph.find_nearest_vertex(rider.start_location)
            dest_node = self.graph.find_nearest_vertex(rider.destination)
            _, ride_duration = find_shortest_path(self.graph, pickup_node, dest_node)
            dropoff_time = pickup_time + ride_duration
            
            rider.wait_time = pickup_time - self.current_time
            rider.trip_duration = ride_duration
            
            # Schedule pickup and dropoff events
            heapq.heappush(self.events, (pickup_time, "pickup_arrival", (best_car, rider)))
            heapq.heappush(self.events, (dropoff_time, "ride_complete", (best_car, rider)))
        
        # Schedule next rider request
        if self.current_time < self.max_time:
            next_request_time = self.current_time + random.expovariate(1.0 / self.mean_arrival_time)
            if next_request_time < self.max_time:
                heapq.heappush(self.events, (next_request_time, "rider_request", None))

    def handle_ride_complete(self, car, rider):
        car.position = rider.destination
        car.available = True
        car.rides_completed += 1
        
        # Store trip data
        self.trip_data.append({
            'rider_id': rider.id,
            'car_id': car.car_id,
            'wait_time': rider.wait_time,
            'trip_duration': rider.trip_duration,
            'completion_time': self.current_time
        })
        
        self.completed_rides.append((rider.id, car.car_id, self.current_time))
        self.quadtree.insert(car.position, car)
        
        print(f"TIME {self.current_time:.2f}: Rider {rider.id} dropped off by Car {car.car_id}")
    
    def handle_pickup_arrival(self, car, rider):
        car.position = rider.start_location
        print(f"TIME {self.current_time:.2f}: Car {car.car_id} picked up Rider {rider.id}")

    def calculate_metrics(self):
        if not self.trip_data:
            return {
                "total_trips": 0,
                "total_riders_generated": self.total_riders_generated,
                "avg_wait_time": 0,
                "avg_trip_duration": 0,
                "rides_per_car": {car.car_id: car.rides_completed for car in self.cars}
            }
        
        total_rides = len(self.trip_data)
        avg_wait = sum(trip['wait_time'] for trip in self.trip_data) / total_rides
        avg_duration = sum(trip['trip_duration'] for trip in self.trip_data) / total_rides
        rides_per_car = {car.car_id: car.rides_completed for car in self.cars}
        
        return {
            "total_trips": total_rides,
            "total_riders_generated": self.total_riders_generated,
            "avg_wait_time": avg_wait,
            "avg_trip_duration": avg_duration,
            "rides_per_car": rides_per_car,
        }

    def create_visualization(self, filename='simulation_summary.png'):
        """Create visualization with matplotlib"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Left side: map with final car positions
        for node_id, neighbors in self.graph.adjacency_list.items():
            x1, y1 = self.graph.node_coordinates[node_id]
            for neighbor_id, _ in neighbors:
                x2, y2 = self.graph.node_coordinates[neighbor_id]
                ax1.plot([x1, x2], [y1, y2], 'lightgray', linewidth=0.5)
        
        car_x = [car.position[0] for car in self.cars]
        car_y = [car.position[1] for car in self.cars]
        ax1.scatter(car_x, car_y, c='red', s=100, marker='s', label='Cars')
        ax1.set_title('Final Car Locations')
        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        ax1.legend()
        ax1.grid(True)
        
        # Right side: simulation results
        metrics = self.calculate_metrics()
        ax2.clear()
        metrics_text = f"""SIMULATION RESULTS

Total Riders: {metrics['total_riders_generated']}
Completed Trips: {metrics['total_trips']}
Avg Wait Time: {metrics['avg_wait_time']:.2f}
Avg Trip Duration: {metrics['avg_trip_duration']:.2f}

RIDES PER CAR:"""
        for car_id, rides in metrics['rides_per_car'].items():
            metrics_text += f"\nCar {car_id}: {rides} rides"
        
        ax2.text(0.1, 0.9, metrics_text, fontsize=10, verticalalignment='top', 
                fontfamily='monospace', transform=ax2.transAxes)
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.show()
        
        print(f"Visualization saved as {filename}")
        return metrics