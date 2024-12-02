"""Solution for day 1 - list distance and similarity."""
from collections import Counter
from typing import List, Tuple


def parse_input(text: str) -> List[Tuple[int, int]]:
    """Parse input string into list of integer pairs."""
    pairs = []
    for line in text.strip().splitlines():
        left, right = line.strip().split()
        pairs.append((int(left), int(right)))
    return pairs


def calculate_total_distance(text: str) -> int:
    """Calculate total distance between sorted pairs from input text.
    
    For part 1:
    - Takes two lists of numbers side by side
    - Sorts each list independently
    - Pairs up numbers by position after sorting
    - Calculates total distance (sum of absolute differences between pairs)
    """
    # Parse input into pairs
    pairs = parse_input(text)
    
    # Split into separate lists and sort
    left = sorted(p[0] for p in pairs)
    right = sorted(p[1] for p in pairs)
    
    # Calculate total distance between corresponding elements
    total = 0
    for l, r in zip(left, right):
        total += abs(l - r)
        
    return total


def calculate_similarity_score(text: str) -> int:
    """Calculate similarity score for part 2.
    
    For each number x in left list:
      - Count how many times it appears in right list (n)
      - Add (x * n) to total score
    """
    pairs = parse_input(text)
    
    # Get lists and count frequencies
    left = [p[0] for p in pairs]
    right_counts = Counter(p[1] for p in pairs)
    
    # Calculate similarity score
    total = 0
    for num in left:
        total += num * right_counts[num]
        
    return total


def solution() -> int:
    """Solve both parts and return final result."""
    # Read full input from stdin
    text = input()
    
    # Run part 1 (total distance)
    distance = calculate_total_distance(text)
    
    # Run part 2 (similarity score)  
    similarity = calculate_similarity_score(text)
    
    # Return either part 1 or part 2 result depending on need
    return distance  # Replace with similarity for part 2