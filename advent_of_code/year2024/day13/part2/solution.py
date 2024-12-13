from typing import Optional, List, Tuple
from dataclasses import dataclass
import re
from fractions import Fraction


@dataclass
class ClawMachine:
    button_a: Tuple[int, int]  # (x, y) movement for button A
    button_b: Tuple[int, int]  # (x, y) movement for button B
    prize: Tuple[int, int]     # (x, y) coordinates of prize


def parse_machine(lines: List[str]) -> ClawMachine:
    """Parse a single claw machine configuration from input lines."""
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    match = re.match(pattern, "\n".join(lines))
    if not match:
        raise ValueError("Invalid input format")
    
    nums = [int(x) for x in match.groups()]
    return ClawMachine(
        button_a=(nums[0], nums[1]),
        button_b=(nums[2], nums[3]),
        prize=(nums[4], nums[5])
    )


def solve_diophantine(a: int, b: int, c: int) -> Optional[Tuple[Fraction, Fraction]]:
    """
    Solves diophantine equation ax + by = c
    Returns (x, y) as fractions if solution exists, None otherwise
    """
    # Use extended Euclidean algorithm
    def gcd_ext(a: int, b: int) -> Tuple[int, int, int]:
        if b == 0:
            return a, 1, 0
        g, x, y = gcd_ext(b, a % b)
        return g, y, x - (a // b) * y

    # Ensure a and b are not both 0
    if a == 0 and b == 0:
        return None if c != 0 else (Fraction(0), Fraction(0))

    g, x0, y0 = gcd_ext(abs(a), abs(b))
    
    # No solution if c is not divisible by gcd
    if c % g != 0:
        return None

    # Adjust signs
    if a < 0:
        x0 = -x0
    if b < 0:
        y0 = -y0

    x = Fraction(x0 * c, g)
    y = Fraction(y0 * c, g)
    
    return x, y


def solve_machine_part2(machine: ClawMachine) -> Optional[Tuple[int, int]]:
    """
    Solve for a single machine, returning (a_presses, b_presses) if solution exists.
    Handles part 2 with large prize coordinates.
    """
    # Extract movement and prize coordinates
    ax, ay = machine.button_a
    bx, by = machine.button_b
    px, py = machine.prize

    # Solve system of equations:
    # ax * A + bx * B = px
    # ay * A + by * B = py
    
    det = ax * by - ay * bx
    if det == 0:
        return None

    # Solve using diophantine equations
    x_solution = solve_diophantine(ax, bx, px)
    y_solution = solve_diophantine(ay, by, py)

    if x_solution is None or y_solution is None:
        return None

    a_x, b_x = x_solution
    a_y, b_y = y_solution

    # Find the intersection of solutions
    if abs(a_x - a_y) > 0.0001 or abs(b_x - b_y) > 0.0001:
        return None
    
    # Convert to integers and verify they are non-negative
    a_presses = round(float(a_x))
    b_presses = round(float(b_x))

    if a_presses < 0 or b_presses < 0:
        return None

    # Verify the solution
    if (a_presses * ax + b_presses * bx == px and
        a_presses * ay + b_presses * by == py):
        return a_presses, b_presses

    return None


def calculate_min_tokens_part2(input_str: str) -> int:
    """Calculate the minimum tokens for part 2."""
    machines_str = [m.strip() for m in input_str.split("\n\n")]
    offset = 10_000_000_000_000
    total_tokens = 0

    for machine_str in machines_str:
        lines = machine_str.split("\n")
        machine = parse_machine(lines)
        machine.prize = (machine.prize[0] + offset, machine.prize[1] + offset)
        result = solve_machine_part2(machine)
        if result:
            a_presses, b_presses = result
            total_tokens += 3 * a_presses + b_presses

    return total_tokens