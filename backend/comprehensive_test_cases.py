"""
Comprehensive Test Cases with Location Support
Tests AI service with proper location context
"""

from ai_service import structure_grievance, classify_department, assign_priority, verify_closure
import json

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test_header(test_num, title):
    print(f"\n{'='*80}")
    print(f"{BLUE}TEST {test_num}: {title}{RESET}")
    print('='*80)

# =============================================================================
# TEST SUITE 1: WITH COMPLETE LOCATION DATA
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("TEST SUITE 1: GRIEVANCES WITH COMPLETE LOCATION DATA")
print(f"{'='*80}{RESET}")

location_tests = [
    {
        "id": 1,
        "title": "Hospital Equipment - Complete Location",
        "text": "No ventilators available. COVID patients suffering.",
        "location": {
            "city": "Mumbai",
            "area": "Parel",
            "pincode": "400012",
            "specificLocation": "KEM Hospital"
        },
        "expected_dept": "Health",
        "expected_priority": "high"
    },
    {
        "id": 2,
        "title": "Road Pothole - Complete Location",
        "text": "Huge pothole causing accidents. 3 bikes damaged this week.",
        "location": {
            "city": "Mumbai",
            "area": "Bandra West",
            "pincode": "400050",
            "specificLocation": "SV Road near Shoppers Stop"
        },
        "expected_dept": "Infrastructure",
        "expected_priority": "high"
    },
    {
        "id": 3,
        "title": "Street Light - Complete Location",
        "text": "Light not working. Dark and unsafe at night.",
        "location": {
            "city": "Mumbai",
            "area": "Andheri East",
            "pincode": "400069",
            "specificLocation": "Sakinaka Metro Station exit"
        },
        "expected_dept": "Public Safety",
        "expected_priority": "medium"
    }
]

for test in location_tests:
    print_test_header(test["id"], test["title"])
    print(f"Grievance: {test['text']}")
    print(f"Location: {test['location']['specificLocation']}, {test['location']['area']}, {test['location']['city']}")
    
    # Test structuring with location
    structured = structure_grievance(test["text"], test["location"])
    print(f"\n{GREEN}Structured Grievance:{RESET}")
    print(structured[:300] + "..." if len(structured) > 300 else structured)
    
    # Test department classification
    dept = classify_department(test["text"], structured)
    print(f"\n{GREEN}Department:{RESET} {dept}")
    print(f"Expected: {test['expected_dept']}")
    
    # Test priority
    priority = assign_priority(test["text"], test["location"])
    print(f"\n{GREEN}Priority:{RESET} {priority}")
    print(f"Expected: {test['expected_priority']}")
    
    # Check if location is in structured output
    has_location = test['location']['specificLocation'].lower() in structured.lower()
    print(f"\n{GREEN if has_location else RED}Location Verification:{RESET} {'✅ Specific location included' if has_location else '❌ Location missing'}")

# =============================================================================
# TEST SUITE 2: WITHOUT LOCATION DATA (Vague Grievances)
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("TEST SUITE 2: GRIEVANCES WITHOUT LOCATION DATA (Should be flagged)")
print(f"{'='*80}{RESET}")

vague_tests = [
    {
        "id": 1,
        "title": "Vague Hospital Complaint",
        "text": "Hospital has no medicines. Patients being turned away.",
        "location": None
    },
    {
        "id": 2,
        "title": "Vague Road Complaint",
        "text": "Road is full of potholes everywhere.",
        "location": None
    },
    {
        "id": 3,
        "title": "Vague Water Complaint",
        "text": "No water supply for many days.",
        "location": None
    }
]

for test in vague_tests:
    print_test_header(test["id"], test["title"])
    print(f"Grievance: {test['text']}")
    print(f"Location: {RED}NOT PROVIDED{RESET}")
    
    structured = structure_grievance(test["text"], test["location"])
    print(f"\n{YELLOW}Structured Grievance (checking for missing location flag):{RESET}")
    print(structured[:400] + "..." if len(structured) > 400 else structured)
    
    # Check if AI flagged missing location
    flagged = "not specified" in structured.lower() or "missing" in structured.lower()
    print(f"\n{GREEN if flagged else RED}Missing Location Detection:{RESET} {'✅ AI flagged missing location' if flagged else '❌ AI did not flag'}")
    
    priority = assign_priority(test["text"], test["location"])
    print(f"\n{YELLOW}Priority:{RESET} {priority} (may be lower due to vague location)")

# =============================================================================
# TEST SUITE 3: PARTIAL LOCATION DATA
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("TEST SUITE 3: PARTIAL LOCATION DATA")
print(f"{'='*80}{RESET}")

partial_tests = [
    {
        "id": 1,
        "title": "City and Area, but No Specific Location",
        "text": "School roof leaking badly. Children getting wet.",
        "location": {
            "city": "Mumbai",
            "area": "Borivali",
            "pincode": "",
            "specificLocation": ""  # Missing!
        }
    },
    {
        "id": 2,
        "title": "Only Specific Location in Text",
        "text": "Garbage not collected at Lokhandwala Market for 2 weeks.",
        "location": {
            "city": "",
            "area": "",
            "pincode": "",
            "specificLocation": ""
        }
    }
]

for test in partial_tests:
    print_test_header(test["id"], test["title"])
    print(f"Grievance: {test['text']}")
    print(f"Location Data: {test['location']}")
    
    structured = structure_grievance(test["text"], test["location"])
    print(f"\n{BLUE}Checking if AI extracts location from text:{RESET}")
    print(structured[:350] + "..." if len(structured) > 350 else structured)

# =============================================================================
# TEST SUITE 4: CLOSURE VERIFICATION WITH LOCATION
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("TEST SUITE 4: CLOSURE VERIFICATION (Location-Aware)")
print(f"{'='*80}{RESET}")

sample_grievance = """**Issue Summary:** Broken street light causing safety concerns

**Location Details:**
- City/Region: Mumbai
- Area/Locality: Andheri West
- Specific Location: Near Sector 5 Park, next to XYZ School
- Pincode: 400058

**Detailed Description:** The street light has been non-functional for 2 weeks.

**Impact:** Affects 200+ residents. Two theft incidents reported."""

sample_location = {
    "city": "Mumbai",
    "area": "Andheri West",
    "pincode": "400058",
    "specificLocation": "Near Sector 5 Park, next to XYZ School"
}

closure_tests = [
    {
        "id": 1,
        "title": "INADEQUATE - No Location Confirmation",
        "closure": "All streetlights in Mumbai have been repaired.",
        "should_approve": False
    },
    {
        "id": 2,
        "title": "INADEQUATE - Wrong Location",
        "closure": "Streetlight repaired at Sector 3 Park, Andheri. Work order #123.",
        "should_approve": False
    },
    {
        "id": 3,
        "title": "INADEQUATE - Vague Promise",
        "closure": "We will look into the Andheri streetlight issue soon.",
        "should_approve": False
    },
    {
        "id": 4,
        "title": "ADEQUATE - Correct Location + Details",
        "closure": "Streetlight near Sector 5 Park, Andheri West (next to XYZ School) repaired on Jan 22. New LED installed. Work order #SL-445. Team: Municipal Electric.",
        "should_approve": True
    },
    {
        "id": 5,
        "title": "ADEQUATE - Correct Location + Timeline",
        "closure": "Light pole at Sector 5 Park area, Andheri West damaged beyond repair. New pole installation scheduled Jan 28. Temporary lighting installed Jan 23. Location: next to XYZ School gate.",
        "should_approve": True
    }
]

closure_correct = 0
closure_total = len(closure_tests)

for test in closure_tests:
    print_test_header(test["id"], test["title"])
    print(f"Closure Notes: {test['closure']}")
    
    result = verify_closure(sample_grievance, test["closure"], sample_location)
    
    print(f"\n{BLUE}AI Response:{RESET}")
    print(json.dumps(result, indent=2))
    print(f"\nExpected: {'✅ APPROVE' if test['should_approve'] else '❌ REJECT'}")
    print(f"AI Decision: {GREEN if result['approved'] else RED}{'✅ APPROVED' if result['approved'] else '❌ REJECTED'}{RESET}")
    
    success = result["approved"] == test["should_approve"]
    if success:
        closure_correct += 1
        print(f"{GREEN}✅ CORRECT DECISION{RESET}")
    else:
        print(f"{RED}❌ INCORRECT DECISION{RESET}")

print(f"\n{BLUE}Closure Verification Accuracy: {closure_correct}/{closure_total} ({(closure_correct/closure_total)*100:.1f}%){RESET}")

# =============================================================================
# TEST SUITE 5: REAL-WORLD SCENARIOS
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("TEST SUITE 5: REAL-WORLD SCENARIOS")
print(f"{'='*80}{RESET}")

real_world = [
    {
        "id": 1,
        "title": "Urgent Medical Emergency with Location",
        "text": "Ambulance service not responding. Called 108 three times. Patient critical.",
        "location": {
            "city": "Mumbai",
            "area": "Kurla West",
            "pincode": "400070",
            "specificLocation": "Building A, Nehru Nagar, Lane 5"
        }
    },
    {
        "id": 2,
        "title": "School Issue with Partial Info",
        "text": "Teacher shortage. 50 students without math teacher for 1 month.",
        "location": {
            "city": "Pune",
            "area": "Kothrud",
            "pincode": "",
            "specificLocation": "Municipal School #23"
        }
    },
    {
        "id": 3,
        "title": "Water Crisis with Community Impact",
        "text": "No water for 1 week. 500 families affected. Tanker not coming.",
        "location": {
            "city": "Delhi",
            "area": "Rohini Sector 15",
            "pincode": "110085",
            "specificLocation": "Blocks A, B, C - Near Main Park"
        }
    }
]

for test in real_world:
    print_test_header(test["id"], test["title"])
    print(f"{BLUE}Scenario:{RESET} {test['text']}")
    print(f"{BLUE}Location:{RESET} {test['location']['specificLocation']}, {test['location']['area']}")
    
    structured = structure_grievance(test["text"], test["location"])
    dept = classify_department(test["text"], structured)
    priority = assign_priority(test["text"], test["location"])
    
    print(f"\n{GREEN}Results:{RESET}")
    print(f"Department: {dept}")
    print(f"Priority: {priority}")
    print(f"\nStructured Preview:")
    print(structured[:250] + "...")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print(f"\n{YELLOW}{'='*80}")
print("📊 FINAL TEST SUMMARY")
print(f"{'='*80}{RESET}")

print(f"""
✅ Complete Location Tests: Tested 3 scenarios
✅ Vague Location Tests: Tested 3 scenarios (AI should flag missing info)
✅ Partial Location Tests: Tested 2 scenarios (AI should extract from text)
✅ Closure Verification: {closure_correct}/{closure_total} correct ({(closure_correct/closure_total)*100:.1f}%)
✅ Real-World Scenarios: Tested 3 scenarios

{GREEN}Key Improvements with Location Support:{RESET}
1. AI now validates location specificity
2. Missing locations are flagged as "NOT SPECIFIED"
3. Closure verification checks for location confirmation
4. Priority adjusted based on location clarity
5. Vague closures without location details are rejected

{YELLOW}What to Watch For:{RESET}
- Grievances without specific location should be flagged
- Closure must mention the EXACT location from grievance
- Generic closures like "all areas covered" should be rejected
- AI should extract location mentions from text when possible

Next Steps:
1. Fine-tune prompts if accuracy < 80%
2. Test with more edge cases
3. Share with backend team for integration
4. Add frontend validation for required location fields
""")

print('='*80)