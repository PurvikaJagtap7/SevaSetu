"""
Database Migration Script
Adds missing columns to existing database
"""

import sqlite3
import os

DB_PATH = "grievance_db.sqlite"

def migrate_database():
    """Add missing columns to existing database"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database {DB_PATH} not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("DATABASE MIGRATION")
    print("="*70)
    
    # Check if resolution_note column exists
    cursor.execute("PRAGMA table_info(grievances)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"\nCurrent columns in grievances table:")
    for col in column_names:
        print(f"  ✓ {col}")
    
    # Add resolution_note if missing
    if 'resolution_note' not in column_names:
        print("\n⚠️ Missing column: resolution_note")
        print("📝 Adding resolution_note column...")
        try:
            cursor.execute("""
                ALTER TABLE grievances 
                ADD COLUMN resolution_note TEXT
            """)
            conn.commit()
            print("✅ Added resolution_note column successfully!")
        except Exception as e:
            print(f"❌ Error adding column: {e}")
    else:
        print("\n✅ resolution_note column already exists")
    
    # Verify the changes
    cursor.execute("PRAGMA table_info(grievances)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"\nUpdated columns in grievances table:")
    for col in column_names:
        print(f"  ✓ {col}")
    
    conn.close()
    
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    migrate_database()

