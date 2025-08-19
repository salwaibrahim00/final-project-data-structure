# graph.py
import collections
import math

class Graph:
    def __init__(self):
        self.adjacency_list = collections.defaultdict(list)
        self.node_coordinates = {}
    
    def load_map_data(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.strip().split(',')
                if len(parts) != 7:
                    continue
                
                start_id, start_x, start_y, end_id, end_x, end_y, weight = parts
                
                self.node_coordinates[start_id] = (float(start_x), float(start_y))
                self.node_coordinates[end_id] = (float(end_x), float(end_y))
                
                self.adjacency_list[start_id].append((end_id, float(weight)))
                self.adjacency_list[end_id].append((start_id, float(weight)))
    
    def find_nearest_vertex(self, point):
        if not self.node_coordinates:
            raise ValueError("No coordinates loaded")
        
        best_node = None
        best_distance = float('inf')
        
        for node_id, (node_x, node_y) in self.node_coordinates.items():
            distance = math.sqrt((point[0] - node_x)**2 + (point[1] - node_y)**2)
            if distance < best_distance:
                best_distance = distance
                best_node = node_id
        
        return best_node
    
    def get_bounds(self):
        if not self.node_coordinates:
            return (0, 0, 7, 7)
        
        x_coords = [coord[0] for coord in self.node_coordinates.values()]
        y_coords = [coord[1] for coord in self.node_coordinates.values()]
        
        return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))