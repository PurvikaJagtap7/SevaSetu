import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

DB_PATH = "grievance_db.sqlite"

# Grievance status stages
STATUS_STAGES = [
    "Pending",
    "Under Review",
    "In Process",
    "On Hold",
    "Resolved",
    "Closed"
]

# Department list - specific departments
DEPARTMENTS = [
    "Public Health Department",
    "Water Supply & Sanitation Department",
    "Electricity Department",
    "Roads & Infrastructure Department",
    "Municipal Corporation",
    "Police Department",
    "Education Department",
    "Transport Department",
    "Housing & Urban Development",
    "Environment & Forest Department"
]

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Admins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            department TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department) REFERENCES departments(name)
        )
    """)
    
    # Departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Grievances table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grievance_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            user_phone TEXT NOT NULL,
            grievance_text TEXT NOT NULL,
            structured_text TEXT,
            department TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            resolution_note TEXT,
            city TEXT,
            state TEXT,
            area TEXT,
            place TEXT,
            image_path TEXT,
            image_analysis TEXT,
            whatsapp_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (department) REFERENCES departments(name)
        )
    """)
    
    # Status history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grievance_id TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            note TEXT,
            updated_by INTEGER,
            updated_by_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (grievance_id) REFERENCES grievances(grievance_id),
            FOREIGN KEY (updated_by) REFERENCES admins(id)
        )
    """)
    
    # Insert departments if they don't exist
    for dept in DEPARTMENTS:
        cursor.execute("""
            INSERT OR IGNORE INTO departments (name, description)
            VALUES (?, ?)
        """, (dept, f"Handles {dept} related grievances"))
    
    # Migrate existing database - add resolution_note if missing
    try:
        cursor.execute("SELECT resolution_note FROM grievances LIMIT 1")
    except sqlite3.OperationalError:
        print("⚠️ Adding resolution_note column to existing database...")
        cursor.execute("ALTER TABLE grievances ADD COLUMN resolution_note TEXT")
        conn.commit()
        print("✅ Migration complete: resolution_note column added")
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def create_user(name, email, phone, password):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute("""
            INSERT INTO users (name, email, phone, password_hash)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, password_hash))
        
        user_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "user_id": user_id}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Email already exists"}
    finally:
        conn.close()

def authenticate_user(email, password):
    """Authenticate user and return user data"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user["password_hash"], password):
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"]
            }
        }
    return {"success": False, "error": "Invalid credentials"}

def create_admin(name, email, password, department):
    """Create a new admin"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify department exists
    cursor.execute("SELECT name FROM departments WHERE name = ?", (department,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "error": "Invalid department"}
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute("""
            INSERT INTO admins (name, email, password_hash, department)
            VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, department))
        
        admin_id = cursor.lastrowid
        conn.commit()
        return {"success": True, "admin_id": admin_id}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Email already exists"}
    finally:
        conn.close()

def authenticate_admin(email, password):
    """Authenticate admin and return admin data"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM admins WHERE email = ?", (email,))
    admin = cursor.fetchone()
    conn.close()
    
    if admin and check_password_hash(admin["password_hash"], password):
        return {
            "success": True,
            "admin": {
                "id": admin["id"],
                "name": admin["name"],
                "email": admin["email"],
                "department": admin["department"]
            }
        }
    return {"success": False, "error": "Invalid credentials"}

def save_grievance(grievance_id, user_id, user_phone, grievance_text, structured_text,
                   department, priority, city, state, area, place, 
                   image_path=None, image_analysis=None, whatsapp_sent=False):
    """Save grievance to database"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify department exists
    cursor.execute("SELECT name FROM departments WHERE name = ?", (department,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "error": "Invalid department"}
    
    # Convert image_analysis to JSON string if it's a dict
    if image_analysis and isinstance(image_analysis, dict):
        image_analysis = json.dumps(image_analysis)
    
    try:
        cursor.execute("""
            INSERT INTO grievances (
                grievance_id, user_id, user_phone, grievance_text, structured_text,
                department, priority, city, state, area, place,
                image_path, image_analysis, whatsapp_sent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            grievance_id, user_id, user_phone, grievance_text, structured_text,
            department, priority, city, state, area, place,
            image_path, image_analysis, whatsapp_sent
        ))
        
        # Add initial status history entry
        cursor.execute("""
            INSERT INTO status_history (grievance_id, old_status, new_status, note, updated_by_type)
            VALUES (?, ?, ?, ?, ?)
        """, (grievance_id, None, "Pending", "Grievance submitted", "system"))
        
        conn.commit()
        conn.close()
        return {"success": True}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "error": "Grievance ID already exists"}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

def get_grievances_by_user(user_id):
    """Get all grievances for a user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM grievances 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    grievances = []
    for row in rows:
        grievances.append({
            "grievance_id": row["grievance_id"],
            "grievance_text": row["grievance_text"],
            "department": row["department"],
            "priority": row["priority"],
            "status": row["status"],
            "city": row["city"],
            "state": row["state"],
            "created_at": row["created_at"]
        })
    
    return grievances

def get_grievances_by_department(department):
    """Get all grievances for a specific department"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT g.*, u.name as user_name, u.email as user_email
        FROM grievances g
        LEFT JOIN users u ON g.user_id = u.id
        WHERE g.department = ? 
        ORDER BY 
            CASE g.priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END,
            g.created_at DESC
    """, (department,))
    
    rows = cursor.fetchall()
    conn.close()
    
    grievances = []
    for row in rows:
        grievance = dict(row)
        if grievance.get("image_analysis"):
            try:
                grievance["image_analysis"] = json.loads(grievance["image_analysis"])
            except:
                pass
        grievances.append(grievance)
    
    return grievances

def get_grievance_by_id(grievance_id):
    """Get a specific grievance by ID with user phone from grievances table"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT g.*, u.name as user_name, u.email as user_email
        FROM grievances g
        LEFT JOIN users u ON g.user_id = u.id
        WHERE g.grievance_id = ?
    """, (grievance_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        grievance = dict(row)
        # user_phone is already in grievances table from the query
        if grievance.get("image_analysis"):
            try:
                grievance["image_analysis"] = json.loads(grievance["image_analysis"])
            except:
                pass
        return grievance
    return None

def update_grievance_status(grievance_id, status, note=None, updated_by=None, updated_by_type="admin"):
    """Update grievance status and add to history"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure resolution_note column exists
    try:
        cursor.execute("SELECT resolution_note FROM grievances LIMIT 1")
    except sqlite3.OperationalError:
        print("⚠️ Adding resolution_note column...")
        cursor.execute("ALTER TABLE grievances ADD COLUMN resolution_note TEXT")
        conn.commit()
    
    # Get current status
    cursor.execute("SELECT status FROM grievances WHERE grievance_id = ?", (grievance_id,))
    current = cursor.fetchone()
    if not current:
        conn.close()
        return {"success": False, "error": "Grievance not found"}
    
    old_status = current["status"]
    
    # Update grievance status
    if note:
        cursor.execute("""
            UPDATE grievances 
            SET status = ?, resolution_note = ?, updated_at = CURRENT_TIMESTAMP
            WHERE grievance_id = ?
        """, (status, note, grievance_id))
    else:
        cursor.execute("""
            UPDATE grievances 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE grievance_id = ?
        """, (status, grievance_id))
    
    # Add to status history
    cursor.execute("""
        INSERT INTO status_history (grievance_id, old_status, new_status, note, updated_by, updated_by_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (grievance_id, old_status, status, note, updated_by, updated_by_type))
    
    conn.commit()
    conn.close()
    return {"success": True, "old_status": old_status, "new_status": status}

def get_status_history(grievance_id):
    """Get status history for a grievance"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sh.*, a.name as admin_name
        FROM status_history sh
        LEFT JOIN admins a ON sh.updated_by = a.id
        WHERE sh.grievance_id = ?
        ORDER BY sh.created_at DESC
    """, (grievance_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_all_grievances():
    """Get all grievances (for super admin)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT g.*, u.name as user_name
        FROM grievances g
        LEFT JOIN users u ON g.user_id = u.id
        ORDER BY g.created_at DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    grievances = []
    for row in rows:
        grievance = dict(row)
        if grievance.get("image_analysis"):
            try:
                grievance["image_analysis"] = json.loads(grievance["image_analysis"])
            except:
                pass
        grievances.append(grievance)
    
    return grievances

def get_departments():
    """Get all departments"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM departments ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_admin_profile_with_stats(admin_id):
    """Get admin profile with statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get admin details
    cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
    admin = cursor.fetchone()
    
    if not admin:
        conn.close()
        return None
    
    department = admin["department"]
    
    # Get total grievances handled
    cursor.execute("""
        SELECT COUNT(*) as total FROM grievances WHERE department = ?
    """, (department,))
    total_handled = cursor.fetchone()["total"]
    
    # Get resolved count
    cursor.execute("""
        SELECT COUNT(*) as resolved FROM grievances 
        WHERE department = ? AND status = 'Resolved'
    """, (department,))
    resolved_count = cursor.fetchone()["resolved"]
    
    # Get pending count
    cursor.execute("""
        SELECT COUNT(*) as pending FROM grievances 
        WHERE department = ? AND status = 'Pending'
    """, (department,))
    pending_count = cursor.fetchone()["pending"]
    
    conn.close()
    
    return {
        "id": admin["id"],
        "name": admin["name"],
        "email": admin["email"],
        "department": admin["department"],
        "position": "Department Admin",
        "governmentUnder": "State Government",
        "totalHandled": total_handled,
        "resolved": resolved_count,
        "pending": pending_count,
        "created_at": admin["created_at"]
    }

def get_admin_dashboard_stats(admin_id):
    """Get comprehensive dashboard statistics for admin's department"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get admin department
    cursor.execute("SELECT department FROM admins WHERE id = ?", (admin_id,))
    admin = cursor.fetchone()
    
    if not admin:
        conn.close()
        return {
            "priorityData": [],
            "deptData": [],
            "trendData": [],
            "grievances": [],
            "statusCounts": {}
        }
    
    department = admin["department"]
    
    # Priority distribution for this department
    cursor.execute("""
        SELECT priority, COUNT(*) as count
        FROM grievances
        WHERE department = ?
        GROUP BY priority
    """, (department,))
    priority_rows = cursor.fetchall()
    priority_data = []
    for row in priority_rows:
        priority_data.append({
            "name": row["priority"].capitalize(),
            "value": row["count"]
        })
    
    # Department comparison (all departments)
    cursor.execute("""
        SELECT department, COUNT(*) as count
        FROM grievances
        GROUP BY department
        ORDER BY count DESC
        LIMIT 5
    """, ())
    dept_rows = cursor.fetchall()
    dept_data = []
    for row in dept_rows:
        dept_name = row["department"].replace(" Department", "").replace("Public ", "").replace(" & ", "/")[:15]
        dept_data.append({
            "dept": dept_name,
            "count": row["count"]
        })
    
    # Daily trend (last 7 days) for this department
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM grievances
        WHERE department = ? AND created_at >= date('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """, (department,))
    trend_rows = cursor.fetchall()
    trend_data = []
    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for row in trend_rows:
        from datetime import datetime
        date_obj = datetime.strptime(row["date"], "%Y-%m-%d")
        day_name = day_names[date_obj.weekday()]
        trend_data.append({
            "day": day_name,
            "count": row["count"]
        })
    
    # Recent grievances for this department
    cursor.execute("""
        SELECT g.*, u.name as user_name
        FROM grievances g
        LEFT JOIN users u ON g.user_id = u.id
        WHERE g.department = ?
        ORDER BY 
            CASE g.priority 
                WHEN 'high' THEN 1 
                WHEN 'medium' THEN 2 
                WHEN 'low' THEN 3 
            END,
            g.created_at DESC
        LIMIT 10
    """, (department,))
    grievance_rows = cursor.fetchall()
    grievances = []
    for row in grievance_rows:
        grievance = dict(row)
        grievances.append({
            "id": grievance["grievance_id"],
            "user": grievance.get("user_name") or "Guest",
            "dept": grievance["department"].split(" ")[0],  # Short name
            "priority": grievance["priority"].capitalize(),
            "status": grievance["status"],
            "date": datetime.strptime(grievance["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d %b"),
        })
    
    # Status counts
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM grievances
        WHERE department = ?
        GROUP BY status
    """, (department,))
    status_rows = cursor.fetchall()
    status_counts = {}
    for row in status_rows:
        status_counts[row["status"]] = row["count"]
    
    conn.close()
    
    return {
        "priorityData": priority_data,
        "deptData": dept_data,
        "trendData": trend_data,
        "grievances": grievances,
        "statusCounts": status_counts,
        "department": department
    }

def seed_sample_data():
    """Add sample users and admins for testing"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Sample Users
    sample_users = [
        {
            "name": "Ramesh Kumar",
            "email": "ramesh@example.com",
            "phone": "+919876543210",
            "password": "password123"
        },
        {
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "phone": "+919876543211",
            "password": "password123"
        },
        {
            "name": "Amit Patel",
            "email": "amit@example.com",
            "phone": "+919876543212",
            "password": "password123"
        }
    ]
    
    # Sample Admins (one for each department)
    sample_admins = [
        {
            "name": "Dr. Rajesh Singh",
            "email": "admin.health@example.com",
            "password": "admin123",
            "department": "Public Health Department"
        },
        {
            "name": "Mr. Vikram Mehta",
            "email": "admin.water@example.com",
            "password": "admin123",
            "department": "Water Supply & Sanitation Department"
        },
        {
            "name": "Ms. Anjali Desai",
            "email": "admin.electricity@example.com",
            "password": "admin123",
            "department": "Electricity Department"
        },
        {
            "name": "Mr. Suresh Reddy",
            "email": "admin.infrastructure@example.com",
            "password": "admin123",
            "department": "Roads & Infrastructure Department"
        },
        {
            "name": "Ms. Kavita Nair",
            "email": "admin.municipal@example.com",
            "password": "admin123",
            "department": "Municipal Corporation"
        },
        {
            "name": "Mr. Deepak Joshi",
            "email": "admin.police@example.com",
            "password": "admin123",
            "department": "Police Department"
        },
        {
            "name": "Ms. Meera Iyer",
            "email": "admin.education@example.com",
            "password": "admin123",
            "department": "Education Department"
        },
        {
            "name": "Mr. Ravi Malhotra",
            "email": "admin.transport@example.com",
            "password": "admin123",
            "department": "Transport Department"
        },
        {
            "name": "Ms. Sunita Rao",
            "email": "admin.housing@example.com",
            "password": "admin123",
            "department": "Housing & Urban Development"
        },
        {
            "name": "Mr. Arjun Menon",
            "email": "admin.environment@example.com",
            "password": "admin123",
            "department": "Environment & Forest Department"
        }
    ]
    
    # Add sample users
    for user in sample_users:
        try:
            cursor.execute("SELECT id FROM users WHERE email = ?", (user["email"],))
            if not cursor.fetchone():
                password_hash = generate_password_hash(user["password"])
                cursor.execute("""
                    INSERT INTO users (name, email, phone, password_hash)
                    VALUES (?, ?, ?, ?)
                """, (user["name"], user["email"], user["phone"], password_hash))
                print(f"✅ Created sample user: {user['email']}")
        except Exception as e:
            print(f"⚠️ Could not create user {user['email']}: {e}")
    
    # Add sample admins
    for admin in sample_admins:
        try:
            cursor.execute("SELECT id FROM admins WHERE email = ?", (admin["email"],))
            if not cursor.fetchone():
                password_hash = generate_password_hash(admin["password"])
                cursor.execute("""
                    INSERT INTO admins (name, email, password_hash, department)
                    VALUES (?, ?, ?, ?)
                """, (admin["name"], admin["email"], password_hash, admin["department"]))
                print(f"✅ Created sample admin: {admin['email']} ({admin['department']})")
        except Exception as e:
            print(f"⚠️ Could not create admin {admin['email']}: {e}")
    
    conn.commit()
    conn.close()

# Initialize database on import
if not os.path.exists(DB_PATH):
    print("\n" + "="*70)
    print("📦 INITIALIZING DATABASE")
    print("="*70)
    init_db()
    print("\n🌱 SEEDING SAMPLE DATA")
    print("="*70)
    seed_sample_data()
    print("="*70)
    print("✅ Database ready! Check TEST_CREDENTIALS.md for login details.\n")
else:
    # Seed sample data even if DB exists (will skip if already exists)
    seed_sample_data()

