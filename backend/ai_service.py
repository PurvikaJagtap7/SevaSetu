import os
import re
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# Utility: Clean Markdown
# -----------------------------
def clean_markdown(text):
    """
    Removes markdown code blocks and formatting from LLM responses
    """
    # Remove code block markers
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** → bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* → italic
    
    # Clean up extra whitespace
    text = text.strip()
    
    return text


def clean_json_response(text):
    """
    Extracts and cleans JSON from LLM response
    """
    # Remove markdown
    text = clean_markdown(text)
    
    # Extract JSON object
    if '{' in text and '}' in text:
        start = text.find('{')
        end = text.rfind('}') + 1
        text = text[start:end]
    
    return text


# -----------------------------
# Core LLM Call
# -----------------------------
def generate_content(prompt, response_format="text"):
    """
    Centralized LLM call using Groq + LLaMA 3
    
    Args:
        prompt: The prompt to send
        response_format: "text" or "json"
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI system for Indian public grievance redressal. "
                    "Your job is to convert informal citizen complaints into "
                    "structured, professional grievance reports suitable for government systems. "
                    "Respond directly without markdown formatting or code blocks."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    
    result = response.choices[0].message.content.strip()
    
    # Clean based on expected format
    if response_format == "json":
        result = clean_json_response(result)
    else:
        result = clean_markdown(result)
    
    return result


# -----------------------------
# 1️⃣ Structure Grievance
# -----------------------------
def structure_grievance(informal_text, location_data=None):
    location_block = ""
    if location_data:
        location_block = f"""
City: {location_data.get('city', 'Not specified')}
Area: {location_data.get('area', 'Not specified')}
Pincode: {location_data.get('pincode', 'Not specified')}
Specific Location: {location_data.get('specificLocation', 'Not specified')}
"""

    prompt = f"""
Convert the following informal grievance into a structured professional grievance report.

Grievance Text:
"{informal_text}"

Location Details (if provided):
{location_block}

Format the response with these sections:

Issue Summary:
[One-line summary]

Detailed Description:
[Clear explanation]

Location Details:
City: [city]
Area: [area]
Specific Location: [specific location or "Not specified"]
Pincode: [pincode or "Not specified"]

Impact:
[Who is affected and how]

Urgency Indicators:
- Duration of Issue: [timeframe]
- Safety Risk: [yes/no and details]
- Vulnerable Population: [if any]
- Confirmed Incidents: [if any]

Expected Resolution:
[What action is needed]

IMPORTANT: Respond with plain text only. Do not use markdown formatting, code blocks, or asterisks for bold/italic.
"""

    return generate_content(prompt, response_format="text")


# -----------------------------
# 2️⃣ Classify Department
# -----------------------------
def classify_department(informal_text, structured_text=None):
    context = structured_text if structured_text else informal_text
    
    prompt = f"""
Based on the grievance below, classify the responsible government department.

Available Departments:
- Health
- Infrastructure
- Electricity
- Water Supply
- Sanitation
- Transport
- Police
- Municipal Services
- Education
- Other

Grievance:
{context}

Respond with ONLY the department name, nothing else. No explanation, no formatting.
"""

    result = generate_content(prompt, response_format="text")
    
    # Extra cleaning: remove any quotes or extra text
    result = result.strip('"\'').strip()
    
    return result


# -----------------------------
# 3️⃣ Assign Priority
# -----------------------------
def assign_priority(informal_text, location_data=None):
    location_hint = ""
    if location_data and location_data.get('specificLocation'):
        location_hint = f"""
Location Context:
City: {location_data.get('city')}
Area: {location_data.get('area')}
Specific Location: {location_data.get('specificLocation')}
"""

    prompt = f"""
Determine the priority level of the grievance below.

Priority Levels:
- high: Safety risk, medical emergency, crime, infrastructure failure, affects many people urgently
- medium: Service delays, moderate impact, no immediate danger
- low: Minor inconvenience, cosmetic issues, affects few people

Grievance:
"{informal_text}"

{location_hint}

Respond with ONLY one word: high, medium, or low
No explanation, no formatting.
"""

    result = generate_content(prompt, response_format="text")
    
    # Ensure lowercase and clean
    result = result.lower().strip('"\'').strip()
    
    # Validate
    if result not in ['high', 'medium', 'low']:
        # Fallback if AI returns something unexpected
        if any(word in informal_text.lower() for word in ['urgent', 'danger', 'emergency', 'critical']):
            result = 'high'
        else:
            result = 'medium'
    
    return result


# -----------------------------
# 4️⃣ Verify Closure
# -----------------------------
def verify_closure(grievance_text, resolution_text, location_data=None):
    location_check = ""
    if location_data and location_data.get('specificLocation'):
        location_check = f"""
Expected Location Reference:
The resolution should confirm action at: {location_data.get('specificLocation')}, {location_data.get('area')}, {location_data.get('city')}
"""

    prompt = f"""
Verify whether the grievance has been satisfactorily resolved.

Original Grievance:
{grievance_text}

{location_check}

Resolution Provided:
{resolution_text}

Evaluation Criteria:
1. Does it address the specific issue?
2. Does it confirm the location mentioned in the grievance?
3. Does it provide specific details (dates, actions taken, work order numbers)?
4. Is it more than just a vague promise?

Inadequate Examples:
- "We will look into it"
- "Issue noted"
- "All areas covered" (without specific location)

Adequate Examples:
- "Streetlight at XYZ Road repaired on Jan 23. Work order #123."
- "Hospital ABC received 3 ventilators on Jan 22. Invoice #456."

Respond ONLY with valid JSON (no markdown, no code blocks):
{{"approved": true, "reason": "brief explanation"}}
OR
{{"approved": false, "reason": "what's missing"}}
"""

    result = generate_content(prompt, response_format="json")
    
    # Parse JSON
    try:
        parsed = json.loads(result)
        
        # Validate structure
        if "approved" in parsed and "reason" in parsed:
            return parsed
        else:
            raise ValueError("Invalid JSON structure")
            
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {result}")
        
        # Fallback
        return {
            "approved": False,
            "reason": "Unable to verify resolution. Please provide specific details including location and actions taken."
        }


# -----------------------------
# Testing
# -----------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("TESTING GROQ AI SERVICE WITH MARKDOWN CLEANING")
    print("=" * 70)
    
    # Test data
    test_location = {
        "city": "Mumbai",
        "area": "Andheri West",
        "pincode": "400058",
        "specificLocation": "Near Sector 5 Park, next to XYZ School"
    }
    
    test_text = "Street light broken for 2 weeks. Very unsafe at night. Kids going to school in dark."
    
    print("\n📝 TEST GRIEVANCE:")
    print(test_text)
    print("\n📍 LOCATION:")
    print(json.dumps(test_location, indent=2))
    
    # Test 1: Structure
    print("\n" + "-" * 70)
    print("1️⃣ STRUCTURE GRIEVANCE:")
    structured = structure_grievance(test_text, test_location)
    print(structured)
    
    # Test 2: Department
    print("\n" + "-" * 70)
    print("2️⃣ CLASSIFY DEPARTMENT:")
    dept = classify_department(test_text, structured)
    print(f"Department: {dept}")
    print(f"Type: {type(dept)}")
    
    # Test 3: Priority
    print("\n" + "-" * 70)
    print("3️⃣ ASSIGN PRIORITY:")
    priority = assign_priority(test_text, test_location)
    print(f"Priority: {priority}")
    print(f"Type: {type(priority)}")
    
    # Test 4: Verify closure (bad)
    print("\n" + "-" * 70)
    print("4️⃣ VERIFY CLOSURE - Bad:")
    bad_closure = "We will check all streetlights in the area."
    result1 = verify_closure(structured, bad_closure, test_location)
    print(f"Closure: {bad_closure}")
    print(f"Result: {json.dumps(result1, indent=2)}")
    
    # Test 5: Verify closure (good)
    print("\n" + "-" * 70)
    print("5️⃣ VERIFY CLOSURE - Good:")
    good_closure = "Streetlight near Sector 5 Park, Andheri West (next to XYZ School) repaired on Jan 23, 2026. New LED installed. Work order #SL-445. Municipal Electric Team."
    result2 = verify_closure(structured, good_closure, test_location)
    print(f"Closure: {good_closure}")
    print(f"Result: {json.dumps(result2, indent=2)}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 70)