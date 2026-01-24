"""
Test script for Admin Profile and Dashboard APIs
Run this after starting the Flask server (python app.py)
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_admin_profile():
    """Test admin profile endpoint"""
    print("\n" + "="*70)
    print("Testing Admin Profile API")
    print("="*70)
    
    # Test with admin ID 1 (should exist from seed data)
    admin_id = 1
    url = f"{BASE_URL}/api/admin/profile/{admin_id}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(json.dumps(data, indent=2))
        else:
            print(f"\n❌ FAILED: {response.text}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure Flask server is running on port 5000")

def test_dashboard_stats():
    """Test dashboard statistics endpoint"""
    print("\n" + "="*70)
    print("Testing Dashboard Stats API")
    print("="*70)
    
    # Test with admin ID 1
    admin_id = 1
    url = f"{BASE_URL}/api/dashboard/stats/{admin_id}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Department: {data['stats'].get('department', 'N/A')}")
            print(f"Priority Data: {data['stats'].get('priorityData', [])}")
            print(f"Department Data: {data['stats'].get('deptData', [])}")
            print(f"Trend Data: {data['stats'].get('trendData', [])}")
            print(f"Grievances Count: {len(data['stats'].get('grievances', []))}")
            print(f"Status Counts: {data['stats'].get('statusCounts', {})}")
        else:
            print(f"\n❌ FAILED: {response.text}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure Flask server is running on port 5000")

def test_grievances_by_department():
    """Test getting grievances by department"""
    print("\n" + "="*70)
    print("Testing Grievances by Department API")
    print("="*70)
    
    department = "Public Health Department"
    url = f"{BASE_URL}/api/grievances/department/{department}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Total Grievances: {len(data['grievances'])}")
            if data['grievances']:
                print("\nFirst Grievance:")
                print(json.dumps(data['grievances'][0], indent=2, default=str))
        else:
            print(f"\n❌ FAILED: {response.text}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure Flask server is running on port 5000")

def test_all_grievances():
    """Test getting all grievances"""
    print("\n" + "="*70)
    print("Testing All Grievances API")
    print("="*70)
    
    url = f"{BASE_URL}/api/grievances/all"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Total Grievances in System: {len(data['grievances'])}")
            if data['grievances']:
                print("\nSample Grievance:")
                g = data['grievances'][0]
                print(f"  ID: {g.get('grievance_id')}")
                print(f"  User: {g.get('user_name', 'Guest')}")
                print(f"  Department: {g.get('department')}")
                print(f"  Priority: {g.get('priority')}")
                print(f"  Status: {g.get('status')}")
                print(f"  Phone: {g.get('user_phone')}")
        else:
            print(f"\n❌ FAILED: {response.text}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Make sure Flask server is running on port 5000")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ADMIN API TESTING SUITE")
    print("="*70)
    print("Make sure Flask server is running: python app.py")
    print("="*70)
    
    test_admin_profile()
    test_dashboard_stats()
    test_grievances_by_department()
    test_all_grievances()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70 + "\n")

