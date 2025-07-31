import random
from quadtree import Quadtree, Rectangle

def brute_force_nearest(points, query):
    best_point = None
    best_dist = float('inf')
    for pt in points:
        dist = ((pt[0] - query[0]) ** 2 + (pt[1] - query[1]) ** 2) ** 0.5
        if dist < best_dist:
            best_point = pt
            best_dist = dist
    return best_point

def main():
    boundary = Rectangle(500, 500, 500, 500)
    qt = Quadtree(boundary)
    points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(5000)]

    for pt in points:
        qt.insert(pt)

    query_point = (random.uniform(0, 1000), random.uniform(0, 1000))

    nearest_quadtree = qt.find_nearest(query_point)
    nearest_bruteforce = brute_force_nearest(points, query_point)

    print(f"Query Point: {query_point}")
    print(f"Nearest by Quadtree: {nearest_quadtree}")
    print(f"Nearest by Brute Force: {nearest_bruteforce}")

    assert nearest_quadtree == nearest_bruteforce, "Mismatch in nearest point results!"

if __name__ == "__main__":
    main()
