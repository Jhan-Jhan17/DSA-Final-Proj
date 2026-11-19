"""
Insertion Sort Implementation
===============================
Ranks available tutors on the Student Dashboard.
The algorithm sorts a list of tutor dictionaries in descending order
based on their star rating (e.g., 4.9 down to 3.5).
"""


def insertion_sort_tutors(tutors):
    """
    Sort a list of tutor dictionaries by rating in DESCENDING order
    using the Insertion Sort algorithm.

    Args:
        tutors (list): A list of dicts, each with at least a 'rating' key.
            Example:
            [
                {'name': 'Tutor A', 'subject': 'Math', 'rating': 4.2},
                {'name': 'Tutor B', 'subject': 'Physics', 'rating': 4.8},
            ]

    Returns:
        list: The same list, sorted in descending order by 'rating'.
    """
    # Create a copy so we don't mutate the original
    sorted_tutors = tutors.copy()

    for i in range(1, len(sorted_tutors)):
        key = sorted_tutors[i]
        j = i - 1

        # Descending order: shift elements that have a SMALLER rating to the right
        while j >= 0 and sorted_tutors[j]['rating'] < key['rating']:
            sorted_tutors[j + 1] = sorted_tutors[j]
            j -= 1

        sorted_tutors[j + 1] = key

    return sorted_tutors
