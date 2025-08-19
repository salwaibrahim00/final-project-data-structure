# Ride-Sharing Simulation

This is my final project  a ride-sharing simulation that puts together all the data structures and algorithms we learned this semester.

## What It Does

The simulation works like Uber - riders request trips and cars pick them up. It uses:
- Quadtree to find nearby cars fast
- Dijkstra's algorithm to plan routes
- Priority queue to handle events in time order
- Graph to represent city streets

## How to Run It

Make sure you have Python and matplotlib installed:

pip install matplotlib


Then just run:

python main.py


You can also change settings:

python main.py --max-time 50 --mean-arrival 4 --map-file map.csv


## Files You Need

- `main.py` - starts everything up
- `simulation.py` - the main simulation code
- `graph.py` - handles the city map
- `quadtree.py` - finds nearby cars
- `dijkstra.py` - calculates shortest paths
- `rider.py` and `car.py` - basic classes
- `map.csv` - the city street data

## What You'll See

The program prints out what's happening:
```
TIME 2.00: Car 3 picked up Rider 1
TIME 4.00: Rider 1 dropped off by Car 3
```

At the end it shows stats like:
- How many trips completed
- Average wait time
- How busy each car was

It also makes a graph called `simulation_summary.png` that shows the map with car positions and all the stats.

## How It Works

When someone requests a ride:
1. Quadtree finds the 5 closest cars
2. Dijkstra's algorithm calculates drive time for each
3. Picks the car with shortest time
4. Schedules pickup and dropoff events

The whole thing runs on a priority queue so events happen in the right order.

## Map File Format

The CSV needs 7 columns: `start_node,start_x,start_y,end_node,end_x,end_y,weight`

## Typical Results

With 5 cars over 50 time units:
- Usually completes 10-15 trips
- Wait times around 2-4 minutes
- Cars end up spread around the map

This shows how the algorithms we studied actually work together to solve real problems like the ones ride-sharing companies face.
