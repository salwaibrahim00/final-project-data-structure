import argparse
import matplotlib.pyplot as plt  # Standard plotting library
from simulation import RideSharingSimulation, Car

def main():
    """Main function to run the ride-sharing simulation"""
    
    # Setup command line options
    parser = argparse.ArgumentParser(description='Ride-sharing simulation')
    parser.add_argument('--max-time', type=float, default=50, help='Max simulation time')
    parser.add_argument('--mean-arrival', type=float, default=4, help='Mean arrival time')
    parser.add_argument('--map-file', type=str, default='map.csv', help='Map file')
    
    args = parser.parse_args()
    
    print("Starting ride-sharing simulation...")
    
    # Create simulation with command line settings
    sim = RideSharingSimulation(
        max_time=args.max_time,
        mean_arrival_time=args.mean_arrival,
        map_file=args.map_file
    )
    
    print(f"Map loaded with {len(sim.graph.node_coordinates)} nodes")
    
    # Add 5 cars at fixed starting positions
    car_locations = [
        (0, 0), (2, 0), (4, 0), (6, 0), (8, 0)
    ]
    
    for i, location in enumerate(car_locations):
        car = Car(i + 1, location)  # Car IDs start at 1
        sim.add_car(car)
    
    print(f"Added {len(car_locations)} cars")
    print("Running simulation...")
    
    # Run the simulation
    sim.run()
    
    # Get results
    metrics = sim.calculate_metrics()
    
    # Print summary
    print(f"\nResults:")
    print(f"Total trips: {metrics['total_trips']}")
    print(f"Total riders: {metrics['total_riders_generated']}")
    print(f"Average wait time: {metrics['avg_wait_time']:.2f}")
    print(f"Average trip duration: {metrics['avg_trip_duration']:.2f}")
    
    # Create and show visualization
    sim.create_visualization()

if __name__ == "__main__":
    main()