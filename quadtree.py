class Rectangle:
    """Helper class to represent a rectangular boundary"""
    def __init__(self, x, y, w, h):
        self.x = x      # center x
        self.y = y      # center y
        self.w = w      # half width
        self.h = h      # half height

    def contains(self, point):
        px, py = point
        return (self.x - self.w <= px <= self.x + self.w and
                self.y - self.h <= py <= self.y + self.h)

    def distance_to_point(self, point):
        px, py = point
        dx = max(abs(px - self.x) - self.w, 0)
        dy = max(abs(py - self.y) - self.h, 0)
        return (dx ** 2 + dy ** 2) ** 0.5


class QuadtreeNode:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w, h = self.boundary.w / 2, self.boundary.h / 2

        self.northwest = QuadtreeNode(Rectangle(x - w, y + h, w, h), self.capacity)
        self.northeast = QuadtreeNode(Rectangle(x + w, y + h, w, h), self.capacity)
        self.southwest = QuadtreeNode(Rectangle(x - w, y - h, w, h), self.capacity)
        self.southeast = QuadtreeNode(Rectangle(x + w, y - h, w, h), self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northwest.insert(point): return True
            if self.northeast.insert(point): return True
            if self.southwest.insert(point): return True
            if self.southeast.insert(point): return True

        return False

    def find_nearest(self, query_point, best=None, best_dist=float('inf')):
        # Prune if this node cannot contain a closer point
        dist_to_boundary = self.boundary.distance_to_point(query_point)
        if dist_to_boundary > best_dist:
            return best, best_dist

        # Check points in this node
        for pt in self.points:
            dist = ((pt[0] - query_point[0]) ** 2 + (pt[1] - query_point[1]) ** 2) ** 0.5
            if dist < best_dist:
                best, best_dist = pt, dist

        # Recursively check children nodes
        if self.divided:
            # Order children so we search the quadrant closest to query_point first
            children = [self.northwest, self.northeast, self.southwest, self.southeast]
            children.sort(key=lambda node: ((node.boundary.x - query_point[0]) ** 2 +
                                            (node.boundary.y - query_point[1]) ** 2) ** 0.5)

            for child in children:
                best, best_dist = child.find_nearest(query_point, best, best_dist)

        return best, best_dist


class Quadtree:
    def __init__(self, boundary, capacity=4):
        self.root = QuadtreeNode(boundary, capacity)

    def insert(self, point):
        return self.root.insert(point)

    def find_nearest(self, query_point):
        best, _ = self.root.find_nearest(query_point)
        return best
