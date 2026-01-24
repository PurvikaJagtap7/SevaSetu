"""
Test Status Update Functionality
Run this after:
1. Starting Flask server (python app.py)
2. Submitting at least one grievance
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_status_update():
    """Test status update endpoint"""
    print("\n" + "="*70)
    print("Testing Status Update")
    print("="*70)
    
    # First, get all grievances to find one to update
    print("\n1️⃣ Fetching all grievances...")
    response = requests.get(f"{BASE_URL}/api/grievances/all")
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch grievances: {response.status_code}")
        print("   Make sure Flask server is running!")
        return
    
    data = response.json()
    grievances = data.get("grievances", [])
    
    if not grievances:
        print("❌ No grievances found in database")
        print("   Please submit a grievance first via the web interface")
        return
    
    # Pick the first grievance
    test_grievance = grievances[0]
    grievance_id = test_grievance["grievance_id"]
    current_status = test_grievance["status"]
    
    print(f"\n✅ Found grievance to test:")
    print(f"   ID: {grievance_id}")
    print(f"   Current Status: {current_status}")
    print(f"   User: {test_grievance.get('user_name', 'Guest')}")
    print(f"   Phone: {test_grievance.get('user_phone')}")
    
    # Determine new status
    status_progression = {
        "Pending": "Under Review",
        "Under Review": "In Process",
        "In Process": "Resolved",
        "Resolved": "Closed",
        "On Hold": "In Process",
        "Closed": "Pending"  # Reset for testing
    }
    
    new_status = status_progression.get(current_status, "Under Review")
    
    print(f"\n2️⃣ Updating status: {current_status} → {new_status}")
    
    # Update status
    update_data = {
        "status": new_status,
        "note": "Test update from automated script",
        "admin_id": 1  # Using admin ID 1 (should exist from seed data)
    }
    
    print(f"\n📤 Sending update request...")
    print(f"   URL: {BASE_URL}/api/grievances/{grievance_id}/status")
    print(f"   Data: {json.dumps(update_data, indent=2)}")
    
    response = requests.put(
        f"{BASE_URL}/api/grievances/{grievance_id}/status",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n📥 Response Status: {response.status_code}")
    
    try:
        result = response.json()
        print(f"\n📋 Response:")
        print(json.dumps(result, indent=2))
        
        if response.status_code == 200 and result.get("status") == "success":
            print("\n✅ SUCCESS! Status updated successfully!")
            
            if result.get("whatsapp_sent"):
                print("📱 WhatsApp notification was sent!")
            elif result.get("whatsapp_error"):
                print(f"⚠️ WhatsApp failed: {result['whatsapp_error']}")
            else:
                print("ℹ️ WhatsApp not configured (this is okay)")
            
            # Verify the update
            print("\n3️⃣ Verifying the update...")
            verify_response = requests.get(f"{BASE_URL}/api/grievances/{grievance_id}")
            
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                updated_grievance = verify_data.get("grievance", {})
                print(f"\n✅ Verification successful!")
                print(f"   Status is now: {updated_grievance.get('status')}")
                print(f"   Resolution note: {updated_grievance.get('resolution_note', 'N/A')}")
            
            # Check status history
            print("\n4️⃣ Checking status history...")
            history_response = requests.get(f"{BASE_URL}/api/grievances/{grievance_id}/history")
            
            if history_response.status_code == 200:
                history_data = history_response.json()
                history = history_data.get("history", [])
                print(f"\n✅ Status history ({len(history)} entries):")
                for entry in history[:3]:  # Show last 3
                    print(f"   • {entry.get('old_status', 'None')} → {entry['new_status']}")
                    print(f"     Note: {entry.get('note', 'N/A')}")
                    print(f"     By: {entry.get('admin_name', 'System')}")
                    print(f"     At: {entry.get('created_at')}")
                    print()
        else:
            print(f"\n❌ FAILED: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ ERROR parsing response: {e}")
        print(f"   Raw response: {response.text}")

def test_invalid_status():
    """Test with invalid status"""
    print("\n" + "="*70)
    print("Testing Invalid Status (should fail gracefully)")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/api/grievances/all")
    if response.status_code != 200:
        print("❌ Cannot fetch grievances")
        return
    
    grievances = response.json().get("grievances", [])
    if not grievances:
        print("❌ No grievances to test with")
        return
    
    grievance_id = grievances[0]["grievance_id"]
    
    # Try invalid status
    print(f"\n📤 Attempting to set invalid status...")
    response = requests.put(
        f"{BASE_URL}/api/grievances/{grievance_id}/status",
        json={
            "status": "Invalid Status",
            "note": "This should fail",
            "admin_id": 1
        },
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    
    if response.status_code == 400 and result.get("status") == "error":
        print("✅ Correctly rejected invalid status!")
        print(f"   Error message: {result.get('message')}")
    else:
        print(f"❌ Should have rejected invalid status!")
        print(f"   Response: {result}")

def test_nonexistent_grievance():
    """Test with non-existent grievance"""
    print("\n" + "="*70)
    print("Testing Non-existent Grievance (should fail gracefully)")
    print("="*70)
    
    fake_id = "GRV999999"
    
    print(f"\n📤 Attempting to update non-existent grievance: {fake_id}")
    response = requests.put(
        f"{BASE_URL}/api/grievances/{fake_id}/status",
        json={
            "status": "Under Review",
            "note": "This should fail",
            "admin_id": 1
        },
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    
    if response.status_code == 404 and result.get("status") == "error":
        print("✅ Correctly rejected non-existent grievance!")
        print(f"   Error message: {result.get('message')}")
    else:
        print(f"❌ Should have rejected non-existent grievance!")
        print(f"   Response: {result}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STATUS UPDATE TEST SUITE")
    print("="*70)
    print("Make sure Flask server is running: python app.py")
    print("="*70)
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Flask server is running\n")
        else:
            print("⚠️ Flask server returned unexpected status\n")
    except:
        print("❌ ERROR: Flask server is not running!")
        print("   Please start it with: cd backend && python app.py\n")
        exit(1)
    
    # Run tests
    test_status_update()
    test_invalid_status()
    test_nonexistent_grievance()
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70 + "\n")

