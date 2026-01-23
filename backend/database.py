import sqlite3
from datetime import datetime
import json

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('grievances.db')
    c = conn.cursor()
    
    # ---------------- USERS TABLE ----------------
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'citizen',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ---------------- GRIEVANCES TABLE ----------------
    c.execute('''
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grievance_id TEXT UNIQUE,
            user_id INTEGER,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            original_text TEXT NOT NULL,
            structured_text TEXT,
            department TEXT,
            priority TEXT,
            status TEXT DEFAULT 'open',
            closure_notes TEXT,
            closure_approved INTEGER DEFAULT 0,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def get_db_connection():
    """Get a connection to the database"""
    conn = sqlite3.connect('grievances.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- USER FUNCTIONS ----------------

def create_user(name, email, password, role='citizen'):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, role))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def authenticate_user(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT id, name, role FROM users
        WHERE email = ? AND password = ?
    ''', (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return {
            'id': user['id'],
            'name': user['name'],
            'role': user['role']
        }
    return None

# ---------------- GRIEVANCE FUNCTIONS ----------------

def generate_grievance_id():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as count FROM grievances')
    count = c.fetchone()['count']
    conn.close()
    return f"GRV{str(count + 1).zfill(3)}"

def save_grievance(data):
    conn = get_db_connection()
    c = conn.cursor()
    grievance_id = generate_grievance_id()

    try:
        c.execute('''
            INSERT INTO grievances 
            (grievance_id, user_id, name, email, phone, original_text, structured_text, department, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            grievance_id,
            data.get('user_id'),
            data['name'],
            data['email'],
            data.get('phone', ''),
            data['original_text'],
            data['structured_text'],
            data['department'],
            data['priority']
        ))
        conn.commit()
        conn.close()
        return grievance_id
    except Exception as e:
        conn.close()
        raise e

def get_grievances_by_department(department):
    conn = get_db_connection()
    c = conn.cursor()

    if department.lower() == 'all':
        c.execute('SELECT * FROM grievances ORDER BY priority DESC, submitted_at DESC')
    else:
        c.execute('''
            SELECT * FROM grievances 
            WHERE department = ? 
            ORDER BY priority DESC, submitted_at DESC
        ''', (department,))

    grievances = c.fetchall()
    conn.close()

    result = []
    for g in grievances:
        result.append({
            'id': g['id'],
            'grievanceId': g['grievance_id'],
            'name': g['name'],
            'email': g['email'],
            'phone': g['phone'],
            'originalText': g['original_text'],
            'structuredText': g['structured_text'],
            'department': g['department'],
            'priority': g['priority'],
            'status': g['status'],
            'closureNotes': g['closure_notes'],
            'closureApproved': bool(g['closure_approved']),
            'submittedAt': g['submitted_at'],
            'closedAt': g['closed_at']
        })
    return result

def get_all_departments():
    return [
        "Health",
        "Education",
        "Infrastructure",
        "Public Safety",
        "Water & Sanitation",
        "Administration",
        "Other"
    ]

def update_grievance_closure(grievance_id, closure_notes, approved):
    conn = get_db_connection()
    c = conn.cursor()

    try:
        if approved:
            c.execute('''
                UPDATE grievances 
                SET closure_notes = ?, 
                    closure_approved = 1, 
                    status = 'closed',
                    closed_at = ?
                WHERE grievance_id = ?
            ''', (closure_notes, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), grievance_id))
        else:
            c.execute('''
                UPDATE grievances 
                SET closure_notes = ?
                WHERE grievance_id = ?
            ''', (closure_notes, grievance_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        raise e

def get_grievance_by_id(grievance_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM grievances WHERE grievance_id = ?', (grievance_id,))
    grievance = c.fetchone()
    conn.close()

    if grievance:
        return {
            'id': grievance['id'],
            'grievanceId': grievance['grievance_id'],
            'name': grievance['name'],
            'email': grievance['email'],
            'phone': grievance['phone'],
            'originalText': grievance['original_text'],
            'structuredText': grievance['structured_text'],
            'department': grievance['department'],
            'priority': grievance['priority'],
            'status': grievance['status'],
            'closureNotes': grievance['closure_notes'],
            'closureApproved': bool(grievance['closure_approved']),
            'submittedAt': grievance['submitted_at'],
            'closedAt': grievance['closed_at']
        }
    return None

if __name__ == "__main__":
    init_db()
