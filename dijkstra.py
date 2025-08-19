# dijkstra.py
# Dijkstra's shortest path algorithm for ride-sharing simulation
import heapq

def find_shortest_path(graph, start_node, end_node):
   """
   Find shortest path between two nodes using Dijkstra's algorithm.
   Returns (path_list, total_distance) or (None, inf) if no path exists.
   """
   # Initialize distances and predecessors
   distances = {node: float('inf') for node in graph.adjacency_list}
   distances[start_node] = 0
   predecessor = {node: None for node in graph.adjacency_list}
   
   # Priority queue: (distance, node)
   heap = [(0, start_node)]
   
   while heap:
       current_distance, current_node = heapq.heappop(heap)
       
       # Early termination when destination reached
       if current_node == end_node:
           break
       
       # Skip if already found shorter path
       if current_distance > distances[current_node]:
           continue
       
       # Check all neighbors
       for neighbor, weight in graph.adjacency_list.get(current_node, []):
           distance = current_distance + weight
           if distance < distances[neighbor]:
               distances[neighbor] = distance
               predecessor[neighbor] = current_node
               heapq.heappush(heap, (distance, neighbor))
   
   # Return None if unreachable
   if distances[end_node] == float('inf'):
       return None, float('inf')
   
   # Reconstruct path
   path = []
   node = end_node
   while node is not None:
       path.insert(0, node)
       node = predecessor[node]
   
   return path, distances[end_node]

def calculate_travel_time_with_graph(graph, start_point, end_point):
   """
   Calculate travel time between coordinate points using road network.
   Maps continuous coordinates to graph nodes and finds optimal route.
   """
   # Map coordinates to nearest graph nodes
   start_node = graph.find_nearest_vertex(start_point)
   end_node = graph.find_nearest_vertex(end_point)
   
   # Find shortest path through road network
   path, travel_time = find_shortest_path(graph, start_node, end_node)
   
   return travel_time, path