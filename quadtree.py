
import math

class Rectangle:
    """My Rectangle class for Quadtree boundaries"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        
    def contains(self, point):
        return (self.x <= point[0] < self.x + self.width and 
                self.y <= point[1] < self.y + self.height)
    
    def intersects(self, other):
        return not (self.x >= other.x + other.width or 
                   other.x >= self.x + self.width or
                   self.y >= other.y + other.height or 
                   other.y >= self.y + self.height)

class Quadtree:
    """
    My Quadtree implementation - enhanced for car management.
    I built this for spatial indexing and now I'm using it for the simulation.
    """
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []  # Store car locations
        self.car_map = {}  # Map locations to car objects - my enhancement
        self.divided = False
        
        # Subdivisions - my original structure
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None
    
    def insert(self, point, car=None):
        """
        Insert a point (car location) into my Quadtree.
        Enhanced to track car objects.
        """
        if not self.boundary.contains(point):
            return False
            
        if car:
            self.car_map[point] = car  # Track the car object
            
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
            
        if not self.divided:
            self.subdivide()
            
        # Try to insert in subdivisions - my recursive approach
        return (self.northwest.insert(point, car) or 
                self.northeast.insert(point, car) or
                self.southwest.insert(point, car) or 
                self.southeast.insert(point, car))
    
    def subdivide(self):
        """My subdivision logic"""
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.width / 2, self.boundary.height / 2
        
        self.northwest = Quadtree(Rectangle(x, y, w, h), self.capacity)
        self.northeast = Quadtree(Rectangle(x + w, y, w, h), self.capacity)
        self.southwest = Quadtree(Rectangle(x, y + h, w, h), self.capacity)
        self.southeast = Quadtree(Rectangle(x + w, y + h, w, h), self.capacity)
        
        self.divided = True
    
    def remove(self, point):
        """
        Remove a point from my Quadtree.
        I added this for when cars get assigned.
        """
        if point in self.points:
            self.points.remove(point)
            if point in self.car_map:
                del self.car_map[point]
            return True
        
        if self.divided:
            return (self.northwest.remove(point) or
                   self.northeast.remove(point) or
                   self.southwest.remove(point) or
                   self.southeast.remove(point))
        
        return False
    
    def find_nearest(self, query_point):
        """My nearest neighbor search - keeping my original implementation"""
        best_point = None
        best_distance = float('inf')
        
        self._find_nearest_recursive(query_point, best_point, best_distance)
        return best_point
    
    def _find_nearest_recursive(self, query_point, best_point, best_distance):
        """My recursive nearest search helper"""
        for point in self.points:
            distance = math.sqrt((point[0] - query_point[0])**2 + 
                               (point[1] - query_point[1])**2)
            if distance < best_distance:
                best_distance = distance
                best_point = point
        
        if self.divided:
            self.northwest._find_nearest_recursive(query_point, best_point, best_distance)
            self.northeast._find_nearest_recursive(query_point, best_point, best_distance)
            self.southwest._find_nearest_recursive(query_point, best_point, best_distance)
            self.southeast._find_nearest_recursive(query_point, best_point, best_distance)
        
        return best_point
    
    def find_k_nearest(self, query_point, k=5):
        """
        Find k nearest points - I enhanced this for the car matching requirement.
        Returns up to k nearest car locations.
        """
        all_points = []
        self._collect_all_points(all_points)
        
        # Calculate distances and sort - my approach
        point_distances = []
        for point in all_points:
            distance = math.sqrt((point[0] - query_point[0])**2 + 
                               (point[1] - query_point[1])**2)
            point_distances.append((distance, point))
        
        # Sort by distance and return k closest
        point_distances.sort()
        return [point for _, point in point_distances[:k]]
    
    def _collect_all_points(self, all_points):
        """Helper to collect all points in the tree"""
        all_points.extend(self.points)
        
        if self.divided:
            self.northwest._collect_all_points(all_points)
            self.northeast._collect_all_points(all_points)
            self.southwest._collect_all_points(all_points)
            self.southeast._collect_all_points(all_points)
    
    def get_car_at_location(self, location):
        """Get the car object at a specific location - my helper method"""
        return self.car_map.get(location)