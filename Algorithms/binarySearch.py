def binary_search(arr, target):
    """
    Performs binary search on a sorted array.
    Returns the index of target if found, otherwise returns None
    Big O Notation: O(log n)
    Space Complexity: O(1)
    """
    low = 0
    high = len(arr) - 1

    print(f"Initial low: {low}, high: {high}")

    while low <= high:
        print(f"Current low: {low}, high: {high}")
        mid = (low + high) // 2  # Rounded down to the nearest integer if the result is a decimal. This is important because array indices must be integers.
        print(f"Checking index: {mid}, value: {arr[mid]}")
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            print(f"Value at index {mid} is greater than target which is {target}. Moving high to back to {mid - 1}")
            high = mid - 1
        else:
            print(f"Value at index {mid} is less than target which is {target}. Moving low to ahead of {mid + 1}")
            low = mid + 1

    return None


# Example usage
if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 7
    result = binary_search(arr, target)
    print(f"Element found at index: {result}")

""" Output:

Initial low: 0, high: 9

Current low: 0, high: 9
Checking index: 4, value: 9
Value at index 4 is greater than target which is 7. Moving high to back to 3

Current low: 0, high: 3
Checking index: 1, value: 3
Value at index 1 is less than target which is 7. Moving low to ahead of 2

Current low: 2, high: 3
Checking index: 2, value: 5
Value at index 2 is less than target which is 7. Moving low to ahead of 3

Current low: 3, high: 3
Checking index: 3, value: 7
Element found at index: 3

"""