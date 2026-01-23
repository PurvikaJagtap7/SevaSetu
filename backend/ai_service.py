from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================= STRUCTURE GRIEVANCE =================
def structure_grievance(text):
    try:
        prompt = f"""
Convert this informal grievance into structured government complaint format with sections:

Issue Summary:
Detailed Description:
Impact/Urgency:
Location:
Expected Resolution:

Grievance: {text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI Error (structure_grievance):", e)
        return "Error structuring grievance"


# ================= CLASSIFY DEPARTMENT =================
def classify_department(text):
    try:
        prompt = f"""
Classify grievance into ONE department only:

Health, Education, Infrastructure, Public Safety, Water & Sanitation, Administration, Other

Return only the department name.

Grievance: {text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        dept = response.choices[0].message.content.strip()

        valid = ["Health","Education","Infrastructure","Public Safety","Water & Sanitation","Administration","Other"]

        for v in valid:
            if v.lower() in dept.lower():
                return v

        return "Other"

    except Exception as e:
        print("AI Error (classify_department):", e)
        return "Other"


# ================= PRIORITY ASSIGN =================
def assign_priority(text):
    try:
        prompt = f"""
Rate urgency as ONLY one word: high, medium, or low.

Grievance: {text}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        p = response.choices[0].message.content.lower()

        if "high" in p:
            return "high"
        if "medium" in p:
            return "medium"
        if "low" in p:
            return "low"

        return "medium"

    except Exception as e:
        print("AI Error (priority):", e)
        return "medium"

# ---------------- VERIFY CLOSURE ---------------- #
def verify_closure(grievance, closure_notes):
    try:
        prompt = f"""
        Check if resolution is valid.

        Grievance:
        {grievance}

        Resolution:
        {closure_notes}

        Return only: APPROVED or REJECTED with reason.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("AI Error (verify_closure):", e)
        return "REJECTED - AI verification failed"
