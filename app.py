"""
SpartanSync: Peer Tutoring Portal
==================================
Batangas State University — The National Engineering University
Academic Year 2026-2027
Core Engine: Custom In-Memory Data Structures
"""

import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from data_structures.priority_queue import MinHeap
from data_structures.interval_bst import IntervalTree
from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.sorting import insertion_sort_tutors

app = Flask(__name__)
app.secret_key = 'spartansync-batstateu-2026-2027-core-key'

# ───────────────────────────────────────────────
# In-Memory Data Structures
# ───────────────────────────────────────────────

request_heap = MinHeap()
schedule_tree = IntervalTree()
session_history = DoublyLinkedList()

# ───────────────────────────────────────────────
# In-Memory Data Registries (Fresh State)
# ───────────────────────────────────────────────

# BSU GSuite domain regex validation
BSU_GSUITE_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@(g\.)?batstate-u\.edu\.ph$', re.IGNORECASE)

# Registered Users Registry
USERS = {
    'maria.santos@g.batstate-u.edu.ph': {
        'name': 'Maria Santos',
        'email': 'maria.santos@g.batstate-u.edu.ph',
        'password': 'password123',
        'role': 'tutor',
        'sr_code': '20-01928',
        'department': 'Computer Engineering',
        'subject': 'Data Structures',
        'rating': 4.9,
        'ratings_list': [5, 5, 5, 4, 5, 5],
        'sessions': 18,
        'location': 'CEA Bldg. Room 304',
        'hourly_rate': 200.00
    },
    'juan.delacruz@g.batstate-u.edu.ph': {
        'name': 'Juan Dela Cruz',
        'email': 'juan.delacruz@g.batstate-u.edu.ph',
        'password': 'password123',
        'role': 'tutor',
        'sr_code': '20-03812',
        'department': 'Computer Engineering',
        'subject': 'Algorithms',
        'rating': 4.7,
        'ratings_list': [5, 4, 5, 5, 4],
        'sessions': 14,
        'location': 'CEA Bldg. Room 302',
        'hourly_rate': 200.00
    },
    'ana.reyes@g.batstate-u.edu.ph': {
        'name': 'Ana Reyes',
        'email': 'ana.reyes@g.batstate-u.edu.ph',
        'password': 'password123',
        'role': 'tutor',
        'sr_code': '20-04910',
        'department': 'General Engineering',
        'subject': 'Calculus',
        'rating': 4.8,
        'ratings_list': [5, 5, 5, 4, 5],
        'sessions': 22,
        'location': 'Math Learning Commons',
        'hourly_rate': 200.00
    },
    'student@g.batstate-u.edu.ph': {
        'name': 'Sample Student',
        'email': 'student@g.batstate-u.edu.ph',
        'password': 'password123',
        'role': 'student',
        'sr_code': '23-08129',
        'department': 'College of Engineering',
        'subject': 'General',
        'rating': 0.0,
        'ratings_list': [],
        'sessions': 0,
        'location': 'Student Center',
        'hourly_rate': 0.00
    }
}

# In-Memory Payments Ledger
PAYMENTS = []

# In-Memory Tutor Disbursements Ledger
DISBURSEMENTS = []

SUBJECTS = [
    'Data Structures',
    'Algorithms',
    'Calculus',
    'Physics',
    'Discrete Mathematics',
    'Object-Oriented Programming',
    'Linear Algebra',
    'Engineering Economics',
    'Differential Equations',
]

URGENCY_LABELS = {
    1: 'Level 1: Urgent (Exam Within 24 Hours)',
    2: 'Level 2: High (Major Task or Quiz This Week)',
    3: 'Level 3: Medium (Homework & Problem Set Help)',
    4: 'Level 4: Standard (Concept Review & Practice)',
    5: 'Level 5: Flexible (General Inquiry)',
}


def get_all_tutors_list():
    """Retrieve list of registered tutors formatted for sorting and display."""
    tutors = []
    for email, u in USERS.items():
        if u.get('role') == 'tutor':
            tutors.append({
                'name': u['name'],
                'email': u['email'],
                'subject': u.get('subject', 'General Academic'),
                'department': u.get('department', 'Academic Affairs'),
                'rating': u.get('rating', 5.0),
                'sessions': u.get('sessions', 0),
                'location': u.get('location', 'Consultation Commons'),
                'hourly_rate': u.get('hourly_rate', 200.00)
            })
    return tutors


# ───────────────────────────────────────────────
# Authentication & Role Routes
# ───────────────────────────────────────────────

@app.route('/')
def index():
    """Portal Landing & Sign-In/Registration Page."""
    if 'user' in session:
        role = session['user'].get('role')
        if role == 'student':
            return redirect(url_for('student_dashboard'))
        elif role == 'tutor':
            return redirect(url_for('tutor_dashboard'))
    return render_template('login.html', active_form=request.args.get('tab', 'login'))


@app.route('/login', methods=['POST'])
def handle_login():
    """Authenticate user with official BatStateU GSuite credentials."""
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()
    selected_role = request.form.get('role', 'student').strip()

    # Domain verification
    if not BSU_GSUITE_PATTERN.match(email):
        flash('Authentication failed: Only official BatStateU GSuite accounts (@g.batstate-u.edu.ph or @batstate-u.edu.ph) are permitted.', 'error')
        return redirect(url_for('index', tab='login'))

    user = USERS.get(email)
    if not user:
        flash('Account not found. Please click the Register GSuite Account tab to create your access credentials.', 'error')
        return redirect(url_for('index', tab='register'))

    if user['password'] != password:
        flash('Incorrect password. Please verify your credentials and try again.', 'error')
        return redirect(url_for('index', tab='login'))

    if user['role'] != selected_role:
        flash(f"Account exists but is registered as '{user['role'].title()}'. Please select the corresponding role.", 'error')
        return redirect(url_for('index', tab='login'))

    # Successful authentication
    session['user'] = {
        'name': user['name'],
        'email': user['email'],
        'role': user['role'],
        'sr_code': user.get('sr_code', 'N/A'),
        'department': user.get('department', 'College of Engineering')
    }
    flash(f"Welcome back, {user['name']}! Signed in as {user['role'].title()}.", 'success')

    if user['role'] == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('tutor_dashboard'))


@app.route('/register', methods=['POST'])
def handle_register():
    """Register a new student or peer tutor using BatStateU GSuite verification."""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', 'student').strip()
    sr_code = request.form.get('sr_code', '').strip()
    department = request.form.get('department', 'College of Engineering').strip()
    subject = request.form.get('subject', 'General Academic').strip()

    # Strict GSuite Validation
    if not BSU_GSUITE_PATTERN.match(email):
        flash('Registration rejected: Only official Batangas State University GSuite accounts (@g.batstate-u.edu.ph or @batstate-u.edu.ph) are accepted.', 'error')
        return redirect(url_for('index', tab='register'))

    if email in USERS:
        flash('An account with this GSuite address already exists. Please proceed to sign in.', 'error')
        return redirect(url_for('index', tab='login'))

    if len(password) < 6:
        flash('Password must be at least 6 characters in length.', 'error')
        return redirect(url_for('index', tab='register'))

    # Create account in user registry
    USERS[email] = {
        'name': name,
        'email': email,
        'password': password,
        'role': role,
        'sr_code': sr_code,
        'department': department,
        'subject': subject if role == 'tutor' else 'Student',
        'rating': 5.0 if role == 'tutor' else 0.0,
        'ratings_list': [5] if role == 'tutor' else [],
        'sessions': 0,
        'location': 'CEA Bldg. Academic Center' if role == 'tutor' else 'Campus Commons',
        'hourly_rate': 200.00 if role == 'tutor' else 0.00
    }

    session['user'] = {
        'name': name,
        'email': email,
        'role': role,
        'sr_code': sr_code,
        'department': department
    }

    flash(f"Account successfully registered with BatStateU GSuite! Welcome to SpartanSync, {name}.", 'success')

    if role == 'student':
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('tutor_dashboard'))


@app.route('/logout')
def logout():
    """Clear session authentication."""
    session.clear()
    flash('You have successfully signed out of SpartanSync.', 'success')
    return redirect(url_for('index'))


# ───────────────────────────────────────────────
# Student Dashboard & Features
# ───────────────────────────────────────────────

@app.route('/student')
def student_dashboard():
    """Student Portal Workspace organized into structured tabs."""
    if 'user' not in session or session['user'].get('role') != 'student':
        flash('Please sign in with your student GSuite account to access this page.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']
    active_tab = request.args.get('tab', 'schedule')

    # Get tutors ranked via Insertion Sort
    raw_tutors = get_all_tutors_list()
    sorted_tutors = insertion_sort_tutors(raw_tutors)

    # Optional tutor search/filter
    selected_subject = request.args.get('subject', '').strip()
    search_query = request.args.get('search', '').strip().lower()

    filtered_tutors = sorted_tutors
    if selected_subject and selected_subject != 'All':
        filtered_tutors = [t for t in filtered_tutors if t['subject'] == selected_subject]
    if search_query:
        filtered_tutors = [
            t for t in filtered_tutors
            if search_query in t['name'].lower() or search_query in t['subject'].lower()
        ]

    # Session history (DLL)
    all_sessions = session_history.get_all()
    # Filter sessions relevant to this student (or show all if fresh)
    student_sessions = [
        s for s in all_sessions
        if s.get('student_email') == current_user['email'] or s.get('student_name') == current_user['name']
    ] if all_sessions else []

    # DLL navigation
    history_size = session_history.get_size()
    history_index = session.get('history_index', 0)

    if history_size > 0:
        if history_index >= history_size:
            history_index = history_size - 1
        elif history_index < 0:
            history_index = 0
        current_record = session_history.get_at_index(history_index)
    else:
        current_record = None

    session['history_index'] = history_index

    # Payments ledger for this student
    student_payments = [
        p for p in PAYMENTS
        if p.get('student_email') == current_user['email'] or p.get('student_name') == current_user['name']
    ]

    total_fees_paid = sum(p['amount'] for p in student_payments if p['status'] == 'Verified / Paid')
    total_fees_pending = sum(p['amount'] for p in student_payments if p['status'] == 'Pending Verification')

    completed_count = sum(1 for s in all_sessions if s.get('status') == 'Completed')
    upcoming_count = sum(1 for s in all_sessions if s.get('status') == 'Upcoming')

    return render_template(
        'student_dashboard.html',
        user=current_user,
        active_tab=active_tab,
        tutors=filtered_tutors,
        all_tutors=sorted_tutors,
        subjects=SUBJECTS,
        selected_subject=selected_subject,
        search_query=search_query,
        history=all_sessions,
        student_sessions=student_sessions,
        current_record=current_record,
        history_index=history_index,
        history_size=history_size,
        schedule=schedule_tree.get_all_intervals(),
        payments=student_payments,
        total_fees_paid=total_fees_paid,
        total_fees_pending=total_fees_pending,
        completed_count=completed_count,
        upcoming_count=upcoming_count,
        urgency_labels=URGENCY_LABELS
    )


@app.route('/book', methods=['POST'])
def book_session():
    """Schedule consultation slot with conflict detection (Interval Tree)."""
    if 'user' not in session or session['user'].get('role') != 'student':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']

    try:
        start = int(request.form.get('start_time', 0))
        end = int(request.form.get('end_time', 0))
        subject = request.form.get('subject', 'General Academic').strip()
        tutor_name = request.form.get('tutor_name', 'Assigned Peer Tutor').strip()
        notes = request.form.get('notes', 'Direct scheduled appointment').strip()
    except (ValueError, TypeError):
        flash('Please enter valid operating hours (07:00 to 21:00).', 'error')
        return redirect(url_for('student_dashboard', tab='schedule'))

    # Check and insert into Interval Tree
    entry_label = f"{subject} &bull; {tutor_name}"
    success, message = schedule_tree.insert(start, end, entry_label)

    if success:
        session_id = f"SES-{202600 + session_history.get_size() + 1}"
        new_session = {
            'session_id': session_id,
            'student_name': current_user['name'],
            'student_email': current_user['email'],
            'tutor': tutor_name,
            'subject': subject,
            'time': f"{start:02d}:00 - {end:02d}:00",
            'location': 'CEA Academic Consultation Center',
            'status': 'Upcoming',
            'notes': notes,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        # Append to Doubly Linked List
        session_history.append(new_session)

        # Create corresponding billing entry (e.g. PHP 200 per session / university subsidized)
        duration_hrs = max(1, end - start)
        session_fee = duration_hrs * 200.00
        payment_record = {
            'payment_id': f"PAY-{len(PAYMENTS) + 1001}",
            'session_id': session_id,
            'student_name': current_user['name'],
            'student_email': current_user['email'],
            'tutor_name': tutor_name,
            'subject': subject,
            'amount': session_fee,
            'status': 'Pending Verification',
            'payment_method': 'Not Selected',
            'reference_no': 'Awaiting Remittance',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        PAYMENTS.append(payment_record)

        flash(f"Appointment booked with {tutor_name} for {subject} ({start:02d}:00 - {end:02d}:00). Consultation record {session_id} generated.", 'success')
        return redirect(url_for('student_dashboard', tab='schedule'))
    else:
        flash(message, 'error')
        return redirect(url_for('student_dashboard', tab='schedule'))


@app.route('/student/request_help', methods=['POST'])
def submit_help_request():
    """Submit urgent academic assistance request into priority queue (Min-Heap)."""
    if 'user' not in session or session['user'].get('role') != 'student':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']
    subject = request.form.get('subject', 'General Academic').strip()
    topic = request.form.get('topic', 'General Consultation').strip()

    try:
        urgency_level = int(request.form.get('urgency_level', 3))
    except (ValueError, TypeError):
        urgency_level = 3

    urgency_label = URGENCY_LABELS.get(urgency_level, 'Level 3: Medium')

    req_data = {
        'student_name': current_user['name'],
        'student_email': current_user['email'],
        'sr_code': current_user.get('sr_code', 'N/A'),
        'subject': subject,
        'topic': topic,
        'urgency_level': urgency_level,
        'urgency_label': urgency_label,
        'date_submitted': datetime.now().strftime('%b %d, %H:%M')
    }

    # Insert into Min-Heap
    request_heap.insert(req_data)

    flash(f"Priority tutoring inquiry for {subject} submitted successfully! Placed at Priority Level {urgency_level}.", 'success')
    return redirect(url_for('student_dashboard', tab='priority'))


@app.route('/student/submit_payment', methods=['POST'])
def submit_payment():
    """Record student payment remittance for a tutoring consultation."""
    if 'user' not in session or session['user'].get('role') != 'student':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    payment_id = request.form.get('payment_id', '').strip()
    payment_method = request.form.get('payment_method', 'Landbank Link.BizPortal').strip()
    reference_no = request.form.get('reference_no', '').strip()

    if not reference_no:
        flash('Please enter the official transaction reference number from your receipt.', 'error')
        return redirect(url_for('student_dashboard', tab='billing'))

    found = False
    for p in PAYMENTS:
        if p['payment_id'] == payment_id:
            p['payment_method'] = payment_method
            p['reference_no'] = reference_no
            p['status'] = 'Verified / Paid'
            found = True
            break

    if found:
        flash(f"Payment verification submitted! Reference {reference_no} recorded for {payment_id}.", 'success')
    else:
        # Create a general payment remittance
        new_pay = {
            'payment_id': f"PAY-{len(PAYMENTS) + 1001}",
            'session_id': 'General Consultation',
            'student_name': session['user']['name'],
            'student_email': session['user']['email'],
            'tutor_name': 'Academic Support Center',
            'subject': 'Tutoring Honorarium Remittance',
            'amount': 200.00,
            'status': 'Verified / Paid',
            'payment_method': payment_method,
            'reference_no': reference_no,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        PAYMENTS.append(new_pay)
        flash(f"Payment receipt {reference_no} recorded successfully.", 'success')

    return redirect(url_for('student_dashboard', tab='billing'))


@app.route('/rate_tutor', methods=['POST'])
def rate_tutor():
    """Submit student evaluation for a peer tutor and update ratings."""
    tutor_name = request.form.get('tutor_name', '').strip()
    try:
        new_rating = int(request.form.get('rating', 5))
    except (ValueError, TypeError):
        new_rating = 5

    found = False
    for email, u in USERS.items():
        if u.get('role') == 'tutor' and u['name'].lower() == tutor_name.lower():
            u['ratings_list'].append(new_rating)
            u['rating'] = round(sum(u['ratings_list']) / len(u['ratings_list']), 1)
            u['sessions'] = u.get('sessions', 0) + 1
            found = True
            break

    if found:
        flash(f"Evaluation recorded for {tutor_name}. Rating updated.", 'success')
    else:
        flash("Tutor record not found.", 'error')

    return redirect(url_for('student_dashboard', tab='tutors'))


# ───────────────────────────────────────────────
# Tutor Dashboard & Features
# ───────────────────────────────────────────────

@app.route('/tutor')
def tutor_dashboard():
    """Peer Tutor Workspace organized into structured tabs."""
    if 'user' not in session or session['user'].get('role') != 'tutor':
        flash('Please sign in with your peer tutor GSuite account to access this page.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']
    active_tab = request.args.get('tab', 'queue')

    # Min-Heap sorted requests
    sorted_requests = request_heap.get_sorted()

    # Session history (DLL)
    all_sessions = session_history.get_all()
    history_size = session_history.get_size()
    history_index = session.get('history_index', 0)

    if history_size > 0:
        if history_index >= history_size:
            history_index = history_size - 1
        elif history_index < 0:
            history_index = 0
        current_record = session_history.get_at_index(history_index)
    else:
        current_record = None

    session['history_index'] = history_index

    # Blocked schedule (Interval Tree)
    blocked_schedule = schedule_tree.get_all_intervals()

    # Tutor's honorarium disbursements
    tutor_disbursements = [
        d for d in DISBURSEMENTS
        if d.get('tutor_email') == current_user['email'] or d.get('tutor_name') == current_user['name']
    ]

    completed_sessions = sum(1 for s in all_sessions if s.get('status') == 'Completed')
    active_inquiries = request_heap.size()

    # Calculate accrued honorarium (PHP 200 per completed session)
    accrued_honorarium = completed_sessions * 200.00
    disbursed_honorarium = sum(d['amount'] for d in tutor_disbursements if d['status'] == 'Disbursed')
    pending_payout = max(0.00, accrued_honorarium - disbursed_honorarium)

    return render_template(
        'tutor_dashboard.html',
        user=current_user,
        active_tab=active_tab,
        requests=sorted_requests,
        heap_size=active_inquiries,
        history=all_sessions,
        current_record=current_record,
        history_index=history_index,
        history_size=history_size,
        blocked_schedule=blocked_schedule,
        disbursements=tutor_disbursements,
        completed_sessions=completed_sessions,
        accrued_honorarium=accrued_honorarium,
        disbursed_honorarium=disbursed_honorarium,
        pending_payout=pending_payout,
        urgency_labels=URGENCY_LABELS,
        subjects=SUBJECTS
    )


@app.route('/accept_request', methods=['POST'])
def accept_request():
    """Accept the top priority student inquiry from the Min-Heap."""
    if 'user' not in session or session['user'].get('role') != 'tutor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']
    top_request = request_heap.pop()

    if top_request:
        session_id = f"SES-{202600 + session_history.get_size() + 1}"
        new_session = {
            'session_id': session_id,
            'student_name': top_request['student_name'],
            'student_email': top_request.get('student_email', 'student@g.batstate-u.edu.ph'),
            'tutor': current_user['name'],
            'subject': top_request['subject'],
            'time': 'Scheduled Immediately (On-Demand)',
            'location': 'CEA Academic Assistance Room / Consultation Desk',
            'status': 'Accepted',
            'notes': f"Assigned from Priority Queue. Topic: {top_request.get('topic', 'General Inquiry')}",
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        # Append to Doubly Linked List
        session_history.append(new_session)

        # Generate billing entry
        payment_record = {
            'payment_id': f"PAY-{len(PAYMENTS) + 1001}",
            'session_id': session_id,
            'student_name': top_request['student_name'],
            'student_email': top_request.get('student_email', 'student@g.batstate-u.edu.ph'),
            'tutor_name': current_user['name'],
            'subject': top_request['subject'],
            'amount': 200.00,
            'status': 'Pending Verification',
            'payment_method': 'Cashier / Digital Remittance',
            'reference_no': 'Awaiting Remittance',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        PAYMENTS.append(payment_record)

        flash(f"Accepted priority consultation for {top_request['student_name']} ({top_request['subject']}). Session {session_id} registered.", 'success')
    else:
        flash('No pending inquiries currently in the priority queue.', 'error')

    return redirect(url_for('tutor_dashboard', tab='queue'))


@app.route('/tutor/block_time', methods=['POST'])
def tutor_block_time():
    """Allow tutors to block unavailable hours in the schedule tree."""
    if 'user' not in session or session['user'].get('role') != 'tutor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']

    try:
        start = int(request.form.get('start_time', 0))
        end = int(request.form.get('end_time', 0))
        reason = request.form.get('reason', 'Reserved Hours').strip() or 'Reserved Hours'
    except (ValueError, TypeError):
        flash('Please enter valid operating hours (07:00 to 21:00).', 'error')
        return redirect(url_for('tutor_dashboard', tab='timetable'))

    success, message = schedule_tree.insert(start, end, f"Blocked: {reason} ({current_user['name']})")
    if success:
        flash(f"Time slot {start:02d}:00 - {end:02d}:00 blocked on public timetable.", 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('tutor_dashboard', tab='timetable'))


@app.route('/tutor/claim_honorarium', methods=['POST'])
def claim_honorarium():
    """Submit a payout disbursement claim for conducted academic tutoring hours."""
    if 'user' not in session or session['user'].get('role') != 'tutor':
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))

    current_user = session['user']
    try:
        amount = float(request.form.get('amount', 200.00))
    except (ValueError, TypeError):
        amount = 200.00

    account_no = request.form.get('account_no', '').strip()
    payout_method = request.form.get('payout_method', 'Landbank ATM Payroll').strip()

    if not account_no:
        flash('Please specify your bank account or e-wallet disbursement number.', 'error')
        return redirect(url_for('tutor_dashboard', tab='honorarium'))

    disbursement_entry = {
        'claim_id': f"CLM-{len(DISBURSEMENTS) + 101}",
        'tutor_name': current_user['name'],
        'tutor_email': current_user['email'],
        'amount': amount,
        'payout_method': payout_method,
        'account_no': account_no,
        'status': 'Disbursed',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    DISBURSEMENTS.append(disbursement_entry)

    flash(f"Honorarium payout claim of PHP {amount:,.2f} via {payout_method} submitted and approved for disbursement.", 'success')
    return redirect(url_for('tutor_dashboard', tab='honorarium'))


@app.route('/update_session_status', methods=['POST'])
def update_session_status():
    """Update status of a session record in the Doubly Linked List."""
    try:
        index = int(request.form.get('index', -1))
        new_status = request.form.get('status', 'Completed').strip()
    except (ValueError, TypeError):
        flash("Invalid request parameters.", 'error')
        return redirect(url_for('index'))

    if 0 <= index < session_history.get_size():
        session_history.update_at_index(index, 'status', new_status)
        flash(f"Consultation status updated to '{new_status}'.", 'success')
    else:
        flash("Record index not found.", 'error')

    role = session.get('user', {}).get('role', 'student')
    if role == 'tutor':
        return redirect(url_for('tutor_dashboard', tab='history'))
    return redirect(url_for('student_dashboard', tab='records'))


@app.route('/navigate_history/<direction>')
def navigate_history(direction):
    """Navigate backwards or forwards through the session history list."""
    history_index = session.get('history_index', 0)
    history_size = session_history.get_size()

    if direction == 'prev' and history_index > 0:
        history_index -= 1
    elif direction == 'next' and history_index < history_size - 1:
        history_index += 1

    session['history_index'] = history_index

    role = session.get('user', {}).get('role', 'student')
    if role == 'tutor':
        return redirect(url_for('tutor_dashboard', tab='history'))
    return redirect(url_for('student_dashboard', tab='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
