"""
Doubly Linked List (DLL) Implementation
=========================================
Stores "Session History". Each node is a completed or upcoming session.
The DLL allows users to traverse their history forward (next) and backward (prev)
seamlessly.
"""


class DLLNode:
    """A node in the Doubly Linked List."""

    def __init__(self, data):
        self.data = data    # Session data (dict)
        self.prev = None    # Pointer to the previous node
        self.next = None    # Pointer to the next node


class DoublyLinkedList:
    """
    A Doubly Linked List that stores session history.
    Supports forward and backward traversal.
    """

    def __init__(self):
        self.head = None    # First node
        self.tail = None    # Last node
        self.size = 0       # Number of nodes

    def append(self, data):
        """
        Append a new session to the end of the list.

        Args:
            data (dict): Session data dictionary.
        """
        new_node = DLLNode(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, data):
        """
        Insert a new session at the beginning of the list.

        Args:
            data (dict): Session data dictionary.
        """
        new_node = DLLNode(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def get_all(self):
        """
        Return all session data as a list (head to tail).

        Returns:
            list: A list of session data dicts.
        """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def get_all_reverse(self):
        """
        Return all session data as a list (tail to head).

        Returns:
            list: A list of session data dicts in reverse order.
        """
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

    def get_at_index(self, index):
        """
        Get the session data at a specific index.

        Args:
            index (int): Zero-based index.

        Returns:
            dict or None: The session data, or None if index is out of bounds.
        """
        if index < 0 or index >= self.size:
            return None

        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def update_at_index(self, index, key, value):
        """
        Update a specific key in the session data at index.

        Args:
            index (int): Zero-based index.
            key (str): Dictionary key to update.
            value (any): New value.

        Returns:
            bool: True if updated, False otherwise.
        """
        if index < 0 or index >= self.size:
            return False

        current = self.head
        for _ in range(index):
            current = current.next
        if current and isinstance(current.data, dict):
            current.data[key] = value
            return True
        return False

    def get_size(self):
        """Return the number of sessions in the list."""
        return self.size

    def is_empty(self):
        """Check if the list is empty."""
        return self.size == 0

    def to_list(self):
        """Alias for get_all — returns all data as a list."""
        return self.get_all()
