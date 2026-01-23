import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def print_test(number, title):
    print(f"\n{'='*70}")
    print(f"🧪 TEST {number}: {title}")
    print(f"{'='*70}")

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")

# TEST 1: Check Backend Running
print_test(1, "Check Backend Running")
try:
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Make sure Flask server is running!")
    exit()

time.sleep(1)

# TEST 2: AI Grievance Processing
print_test(2, "AI Grievance Processing (IMPORTANT)")
data = {
    "text": "Open manholes near my house are dangerous for children"
}
try:
    response = requests.post(f"{BASE_URL}/api/process", json=data)
    print_response(response)
    
    if response.status_code == 200:
        ai_result = response.json()
        structured = ai_result.get("structured", "")
        department = ai_result.get("department", "")
        priority = ai_result.get("priority", "")
    else:
        print("⚠️ Cannot proceed with other tests")
        exit()
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit()

time.sleep(1)

# TEST 3: Submit Grievance to Database
print_test(3, "Submit Grievance to Database")
submit_data = {
    "name": "Purvika",
    "email": "purvika@gmail.com",
    "phone": "9999999999",
    "original_text": "Open manholes near my house",
    "structured_text": structured,
    "department": department,
    "priority": priority
}
try:
    response = requests.post(f"{BASE_URL}/api/submit", json=submit_data)
    print_response(response)
    
    if response.status_code == 200:
        grievance_id = response.json().get("grievanceId", "")
    else:
        print("⚠️ Cannot proceed with closure test")
        grievance_id = None
except Exception as e:
    print(f"❌ ERROR: {e}")
    grievance_id = None

time.sleep(1)

# TEST 4: Get Grievances
print_test(4, "Get Grievances by Department")
try:
    response = requests.get(f"{BASE_URL}/api/grievances/{department}")
    print_response(response)
except Exception as e:
    print(f"❌ ERROR: {e}")

time.sleep(1)

# TEST 5: Get All Departments
print_test(5, "Get All Departments")
try:
    response = requests.get(f"{BASE_URL}/api/departments")
    print_response(response)
except Exception as e:
    print(f"❌ ERROR: {e}")

time.sleep(1)

# TEST 6: AI Closure Verification (Good Resolution)
if grievance_id:
    print_test(6, "AI Closure Verification - GOOD Resolution")
    close_data = {
        "grievanceId": grievance_id,
        "closureNotes": "Manholes covered with steel lids and warning signs installed. Site inspected on Jan 23, 2026. Safety barriers placed around the area."
    }
    try:
        response = requests.post(f"{BASE_URL}/api/close", json=close_data)
        print_response(response)
        print("\n🔥 AI should APPROVE this - it's detailed and specific!")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    time.sleep(1)

    # TEST 7: Submit another grievance for bad closure test
    print_test(7, "Submit Another Grievance for Bad Closure Test")
    submit_data2 = {
        "name": "Test User",
        "email": "test@gmail.com",
        "phone": "8888888888",
        "original_text": "Street light not working",
        "structured_text": "Issue: Street light is broken and needs repair",
        "department": "Infrastructure",
        "priority": "medium"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/submit", json=submit_data2)
        print_response(response)
        
        if response.status_code == 200:
            grievance_id_2 = response.json().get("grievanceId", "")
        else:
            grievance_id_2 = None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        grievance_id_2 = None

    time.sleep(1)

    # TEST 8: AI Closure Verification (Bad Resolution)
    if grievance_id_2:
        print_test(8, "AI Closure Verification - BAD Resolution")
        bad_close_data = {
            "grievanceId": grievance_id_2,
            "closureNotes": "Problem solved"
        }
        try:
            response = requests.post(f"{BASE_URL}/api/close", json=bad_close_data)
            print_response(response)
            print("\n😈 AI should REJECT this - it's too vague!")
        except Exception as e:
            print(f"❌ ERROR: {e}")

print("\n" + "="*70)
print("🎉 ALL TESTS COMPLETED!")
print("="*70)
print("\n📊 Summary:")
print("✅ If all tests passed, your backend is READY for frontend!")
print("✅ You can now share API documentation with your frontend team")
print("✅ Flask server should be running at http://127.0.0.1:5000")