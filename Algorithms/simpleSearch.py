"""
Linear Search Algorithm

A simple search algorithm that checks every element in a sequence
sequentially until the target is found or the end is reached.

Time Complexity: O(n)
Space Complexity: O(1)

Best for: Unsorted arrays, small datasets
"""


def simple_search(arr, target):
    """
    Performs linear search to find a target value in a list.
    
    Args:
        arr: List of elements to search through
        target: The element to find
        
    Returns:
        Index of the target element if found, -1 otherwise
    """
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print("Starting linear search...")
    for i in range(len(arr)):
        print(f"Checking index: {i}, value: {arr[i]}")
        if arr[i] == target:
            return i
    return -1


def simple_search_all(arr, target):
    """
    Finds all occurrences of a target value in a list.
    
    Args:
        arr: List of elements to search through
        target: The element to find
        
    Returns:
        List of indices where target is found, empty list if not found
    """
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print("Starting linear search for all occurrences...")
    indices = []
    for i in range(len(arr)):
        print(f"Checking index: {i}, value: {arr[i]}")
        if arr[i] == target:
            indices.append(i)
    return indices


if __name__ == "__main__":
    # Example usage
    numbers = [10, 5, 23, 7, 45, 2, 45]
    
    print("Array in main:", numbers)
    print("Find 45:", simple_search(numbers, 45))
    print("Find 100:", simple_search(numbers, 100))
    print("Find all occurrences of 45:", simple_search_all(numbers, 45))