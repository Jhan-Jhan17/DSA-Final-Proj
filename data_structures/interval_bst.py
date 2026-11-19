"""
Interval Tree (via BST) Implementation
========================================
Manages the booking schedule to prevent overlapping sessions.
When a student books a slot (e.g., 14:00 to 15:00), the tree checks for
intersections with existing nodes. If it overlaps, the booking is rejected.
"""


class IntervalNode:
    """A single node in the Interval BST."""

    def __init__(self, start, end, subject=""):
        self.start = start      # Start time as integer (e.g., 14 for 14:00)
        self.end = end           # End time as integer (e.g., 15 for 15:00)
        self.subject = subject   # Subject or reason for the block/session
        self.max_end = end       # Maximum end time in subtree
        self.left = None
        self.right = None


class IntervalTree:
    """
    A Binary Search Tree that stores time intervals and detects overlaps.
    Used to manage tutoring session bookings and prevent conflicts.
    """

    def __init__(self):
        self.root = None

    def _overlaps(self, start1, end1, start2, end2):
        """
        Check if two intervals [start1, end1) and [start2, end2) overlap.

        Returns:
            bool: True if the intervals overlap.
        """
        return start1 < end2 and start2 < end1

    def _search_overlap(self, node, start, end):
        """
        Recursively search for any overlapping interval in the tree.

        Args:
            node (IntervalNode): Current node being checked.
            start (int): Start time of the new interval.
            end (int): End time of the new interval.

        Returns:
            IntervalNode or None: The conflicting node, or None if no overlap.
        """
        if node is None:
            return None

        # Check if current node overlaps
        if self._overlaps(node.start, node.end, start, end):
            return node

        # If left child exists and its max_end is greater than our start,
        # there might be an overlap in the left subtree
        if node.left and node.left.max_end > start:
            result = self._search_overlap(node.left, start, end)
            if result:
                return result

        # Otherwise, check right subtree
        return self._search_overlap(node.right, start, end)

    def _insert_node(self, node, new_node):
        """
        Recursively insert a new interval node into the BST.

        Args:
            node (IntervalNode): Current root of the subtree.
            new_node (IntervalNode): The new node to insert.

        Returns:
            IntervalNode: The root of the modified subtree.
        """
        if node is None:
            return new_node

        # Insert based on start time
        if new_node.start < node.start:
            node.left = self._insert_node(node.left, new_node)
        else:
            node.right = self._insert_node(node.right, new_node)

        # Update max_end
        if node.max_end < new_node.end:
            node.max_end = new_node.end

        return node

    def insert(self, start, end, subject=""):
        """
        Attempt to insert a new interval into the tree.

        Args:
            start (int): Start time (24h format, e.g., 14 for 14:00).
            end (int): End time (24h format, e.g., 15 for 15:00).
            subject (str): Subject or purpose for the session.

        Returns:
            tuple: (success: bool, message: str)
                - (True, "Success: Slot Booked!") if no conflict.
                - (False, "Error: Conflict Detected ...") if overlap found.
        """
        # Validate input
        if start >= end:
            return (False, "Error: Start time must be strictly earlier than end time.")

        if start < 7 or end > 21:
            return (False, "Error: Tutoring hours are restricted to 07:00 through 21:00.")

        # Check for overlaps
        conflict = self._search_overlap(self.root, start, end)
        if conflict:
            return (
                False,
                f"Schedule Conflict: Time slot overlaps with an existing appointment "
                f"({conflict.start:02d}:00 - {conflict.end:02d}:00: {conflict.subject})."
            )

        # No conflict — insert the new interval
        new_node = IntervalNode(start, end, subject)
        self.root = self._insert_node(self.root, new_node)
        return (True, "Success: Appointment slot confirmed!")

    def _inorder(self, node, result):
        """Collect all intervals via inorder traversal."""
        if node is None:
            return
        self._inorder(node.left, result)
        result.append({
            'start': node.start,
            'end': node.end,
            'subject': node.subject,
            'display': f"{node.start:02d}:00 - {node.end:02d}:00"
        })
        self._inorder(node.right, result)

    def get_all_intervals(self):
        """
        Return all booked intervals sorted by start time.

        Returns:
            list: A list of dicts with keys: start, end, subject, display.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def is_empty(self):
        """Check if the tree has no bookings."""
        return self.root is None
