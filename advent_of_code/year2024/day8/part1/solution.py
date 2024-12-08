"""
Count antinodes in a grid based on antenna positions and frequencies.

An antinode occurs at a point that is collinear with two antennas of the same frequency 
where one antenna is twice as far from the point as the other.
"""
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import math

def get_antennas(grid: str) -> Dict[str, List[Tuple[int, int]]]:
    """Parse grid to get antenna positions by frequency."""
    antennas = defaultdict(list)
    for y, line in enumerate(grid.strip().splitlines()):
        for x, char in enumerate(line):
            if char != '.':
                antennas[char].append((x, y))
    return antennas

def is_twice_distance(p1: Tuple[float, float], p2: Tuple[float, float], 
                     p3: Tuple[float, float]) -> bool:
    """Check if p2 is twice as far from p1 as p3 is from p1."""
    d1 = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    d2 = math.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2)
    if d1 == 0 or d2 == 0:
        return False

    return abs(d1 / d2 - 2) < 1e-10 or abs(d2 / d1 - 2) < 1e-10

def are_collinear(p1: Tuple[float, float], p2: Tuple[float, float], 
                  p3: Tuple[float, float]) -> bool:
    """Check if three points are collinear."""
    # Using the area of triangle formed by three points
    area = p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
    return abs(area) < 1e-10

def find_antinode(p1: Tuple[int, int], p2: Tuple[int, int]) -> List[Tuple[float, float]]:
    """Find antinodes for two antennas of same frequency."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    if dx == 0 and dy == 0:
        return []

    antinodes = []
    for ratio in [1/3, 3]:
        antinode_x = p1[0] + dx * ratio
        antinode_y = p1[1] + dy * ratio
        antinodes.append((antinode_x, antinode_y))

    return antinodes

def get_grid_bounds(grid: str) -> Tuple[int, int]:
    """Get width and height of grid."""
    lines = grid.strip().splitlines()
    return len(lines[0]), len(lines)

def count_antinodes(grid: str) -> int:
    """Count unique antinode locations within grid bounds."""
    width, height = get_grid_bounds(grid)
    antennas = get_antennas(grid)
    antinodes: Set[Tuple[float, float]] = set()
    
    # Find antinodes for each pair of same-frequency antennas
    for freq, positions in antennas.items():
        for i, p1 in enumerate(positions):
            for p2 in positions[i+1:]:
                # Find potential antinodes
                for antinode in find_antinode(p1, p2):
                    x, y = antinode
                    if 0 <= x < width and 0 <= y < height:
                        # Verify this is a valid antinode
                        if are_collinear(p1, p2, antinode) and \
                           is_twice_distance(antinode, p1, p2):
                            antinodes.add(antinode)
                            
    return len(antinodes)

def solution() -> int:
    """Read input from stdin and solve the problem."""
    import sys
    grid = sys.stdin.read()
    return count_antinodes(grid)

if __name__ == "__main__":
    print(solution())
