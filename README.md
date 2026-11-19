# SpartanSync: Peer Tutoring Portal

**SpartanSync** is an institutional academic consultation and peer tutoring web application developed for **Batangas State University — The National Engineering University** for **Academic Year 2026–2027**.

The application features a complete backend built entirely in Python using **Flask**, styled with **Tailwind CSS** in BatStateU's Crimson (`#8A1538`) and White color palette. The core backend operations are powered by custom, in-memory **Data Structures and Algorithms** without a traditional SQL database.

---

## Data Structures & Algorithms Alignment

- **Min-Heap (Priority Queue)** (`data_structures/priority_queue.py`):
  Manages the tutor's pending student inquiries queue. Inquiries are prioritized strictly by academic urgency level (e.g., Level 1: Exam within 24 hours).
- **Interval Tree / BST** (`data_structures/interval_bst.py`):
  Manages the consultation schedule timetable to detect and prevent overlapping appointments.
- **Doubly Linked List** (`data_structures/doubly_linked_list.py`):
  Maintains the consultation history records, enabling forward and backward record inspection.
- **Insertion Sort** (`data_structures/sorting.py`):
  Ranks accredited peer educators on the portal in descending order based on student ratings.

---

## Directory Structure

```text
SpartanSync/
├── requirements.txt
├── app.py                      # Flask routing & application logic
├── data_structures/            # Custom in-memory DSA implementations
│   ├── __init__.py
│   ├── priority_queue.py       # Min-Heap implementation
│   ├── interval_bst.py         # Interval Tree (via BST)
│   ├── doubly_linked_list.py   # Doubly Linked List
│   └── sorting.py              # Insertion Sort algorithm
├── static/
│   ├── css/
│   │   └── styles.css          # Portal styles
│   ├── js/
│   │   └── app.js              # Tab & dialog interactivity
│   └── img/
│       └── spartansync_logo.png # Official transparent seal
└── templates/
    ├── base.html               # Master layout
    ├── login.html              # GSuite authentication & registration
    ├── student_dashboard.html  # Student consultation workspace (tabs)
    └── tutor_dashboard.html    # Peer educator workspace (tabs)
```

---

## Setup & Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the portal:**
   ```bash
   python app.py
   ```

3. **Access the portal:**
   Open your browser and navigate to `http://127.0.0.1:5000`.
