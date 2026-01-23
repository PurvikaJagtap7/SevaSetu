import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# Core LLM Call
# -----------------------------
def generate_content(prompt):
    """
    Centralized LLM call using Groq + LLaMA 3
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI system for Indian public grievance redressal. "
                    "Your job is to convert informal citizen complaints into "
                    "structured, professional grievance reports suitable for government systems."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


# -----------------------------
# 1️⃣ Structure Grievance
# -----------------------------
def structure_grievance(informal_text, location_data=None):
    location_block = ""
    if location_data:
        location_block = f"""
City: {location_data.get('city')}
Area: {location_data.get('area')}
Pincode: {location_data.get('pincode')}
Specific Location: {location_data.get('specificLocation')}
"""

    prompt = f"""
Convert the following informal grievance into a structured professional grievance report.

Grievance Text:
"{informal_text}"

Location Details (if provided):
{location_block}

Format strictly as:

**Grievance Report**

**1. Issue Summary:**
...

**2. Detailed Description:**
...

**3. Location Details:**
...

**4. Impact:**
...

**5. Urgency Indicators:**
- Duration of Issue
- Safety Risk
- Vulnerable Population
- Confirmed Incidents (if any)

**6. Expected Resolution:**
...

Do not add extra explanations.
"""

    return generate_content(prompt)


# -----------------------------
# 2️⃣ Classify Department
# -----------------------------
def classify_department(informal_text, structured_text):
    prompt = f"""
Based on the grievance below, classify the responsible government department.
Choose ONLY ONE from:
Health, Infrastructure, Electricity, Water Supply, Sanitation, Transport, Police, Municipal Services, Education, Other

Grievance:
{structured_text}

Return only the department name.
"""

    return generate_content(prompt)


# -----------------------------
# 3️⃣ Assign Priority
# -----------------------------
def assign_priority(informal_text, location_data=None):
    location_hint = ""
    if location_data:
        location_hint = f"""
Location Context:
City: {location_data.get('city')}
Area: {location_data.get('area')}
"""

    prompt = f"""
Determine the priority level of the grievance below.
Choose only one: low, medium, high

Grievance:
"{informal_text}"

{location_hint}

Rules:
- Safety risk, medical issues, crime, or infrastructure failures → high
- Service delays without danger → medium
- Minor inconvenience → low

Return only the priority.
"""

    return generate_content(prompt)


# -----------------------------
# 4️⃣ Verify Closure (Optional)
# -----------------------------
def verify_closure(grievance_text, resolution_text):
    prompt = f"""
Verify whether the grievance has been satisfactorily resolved.

Grievance:
{grievance_text}

Resolution Provided:
{resolution_text}

Respond strictly in JSON:
{{
  "approved": true/false,
  "reason": "short justification"
}}
"""

    return generate_content(prompt)
