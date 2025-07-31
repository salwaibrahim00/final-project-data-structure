# Finding Nearest Neighbors Fast with Quadtrees

## What I Built

I was dealing with finding the closest point to some location in 2D space, and checking every single point was getting really slow once I hit thousands of them. So I built this thing called a Quadtree that basically chops up the space into squares and only bothers looking in the squares that matter. Way faster.

Here's what I ended up with:

- Rectangle class - just handles the boundaries of areas
- QuadtreeNode class - holds points and when it gets too full, splits into 4 pieces
- Quadtree class - does the actual work of adding points and finding neighbors

## How It Works

The quadtree sort of maintains itself. When I dump too many points into one spot, it automatically breaks that area into 4 smaller areas and spreads things out.

For finding the nearest point to somewhere, it doesn't waste time. It starts from the top and dives down to wherever looks promising. If there's a whole chunk of space that obviously can't have anything closer than what it already found, it just ignores that chunk completely. 

Way better than the dumb approach of just checking everything.

## Testing

I threw together a test with 5,000 random points. Ran it two ways - my quadtree way and the slow way that checks every single point. Got the same answers both times, so at least I know it's not broken. Mine just runs way faster obviously.
How to Run It
Make sure you have Python 3 installed.

Run the test script by typing:

python test_quadtree.py
It’ll print out the query point and the nearest results from both methods, and double-check that they match.
