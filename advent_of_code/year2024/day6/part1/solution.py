from typing import List, Set, Tuple
import sys
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def right(self):
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP
        }[self]


def find_start(grid: List[str]) -> Tuple[int, int, Direction]:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                return x, y, Direction.UP
            elif cell == '>':
                return x, y, Direction.RIGHT
            elif cell == 'v':
                return x, y, Direction.DOWN
            elif cell == '<':
                return x, y, Direction.LEFT
    raise ValueError("No starting position found")


def count_visited_cells(input_str: str) -> int:
    # Parse grid
    grid = [line.strip() for line in input_str.strip().split('\n')]
    width = len(grid[0])
    height = len(grid)

    # Find starting position and direction
    start_x, start_y, direction = find_start(grid)

    # Track visited positions
    visited: Set[Tuple[int, int]] = {(start_x, start_y)}
    x, y = start_x, start_y
    current_direction = direction

    while True:
        # Calculate next position
        dx, dy = current_direction.value
        next_x, next_y = x + dx, y + dy

        # Check if we're leaving the grid
        if not (0 <= next_x < width and 0 <= next_y < height):
            break

        # Check if there's an obstacle in front
        if grid[next_y][next_x] == '#':
            # Turn right
            current_direction = current_direction.right()
        else:
            # Move forward
            x, y = next_x, next_y
            visited.add((x, y))

    return len(visited)


def solution() -> int:
    # Read input from stdin
    input_data = sys.stdin.read()
    return count_visited_cells(input_data)


if __name__ == "__main__":
    print(solution())