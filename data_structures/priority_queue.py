"""
Min-Heap (Priority Queue) Implementation
==========================================
Manages the Tutor's "Pending Requests" queue.
Requests are objects containing student_name, subject, and urgency_level.
A lower integer means higher urgency (e.g., 1 = Exam Tomorrow, 3 = Homework Help).
The heap always serves the most urgent request first.
"""


class MinHeap:
    """A Min-Heap priority queue built from scratch."""

    def __init__(self):
        self.heap = []

    def _parent(self, index):
        """Return the parent index."""
        return (index - 1) // 2

    def _left_child(self, index):
        """Return the left child index."""
        return 2 * index + 1

    def _right_child(self, index):
        """Return the right child index."""
        return 2 * index + 2

    def _swap(self, i, j):
        """Swap two elements in the heap."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """Restore heap property by bubbling up."""
        while index > 0:
            parent = self._parent(index)
            if self.heap[index]['urgency_level'] < self.heap[parent]['urgency_level']:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _heapify_down(self, index):
        """Restore heap property by bubbling down."""
        size = len(self.heap)
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < size and self.heap[left]['urgency_level'] < self.heap[smallest]['urgency_level']:
                smallest = left
            if right < size and self.heap[right]['urgency_level'] < self.heap[smallest]['urgency_level']:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def insert(self, request):
        """
        Insert a new request into the priority queue.

        Args:
            request (dict): A dictionary with keys:
                - student_name (str)
                - subject (str)
                - urgency_level (int): Lower = more urgent
        """
        self.heap.append(request)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """
        Remove and return the most urgent request (root of the heap).

        Returns:
            dict or None: The most urgent request, or None if the heap is empty.
        """
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self):
        """
        View the most urgent request without removing it.

        Returns:
            dict or None: The most urgent request, or None if the heap is empty.
        """
        return self.heap[0] if self.heap else None

    def get_sorted(self):
        """
        Return all requests sorted by urgency (ascending) without destroying the heap.

        Returns:
            list: A list of request dicts sorted by urgency_level.
        """
        # Create a temporary copy and extract in order
        temp_heap = MinHeap()
        temp_heap.heap = self.heap.copy()
        sorted_requests = []
        while temp_heap.heap:
            sorted_requests.append(temp_heap.pop())
        return sorted_requests

    def size(self):
        """Return the number of elements in the heap."""
        return len(self.heap)

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0
