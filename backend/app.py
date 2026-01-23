from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db
import ai_service as ai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
db.init_db()

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Grievance API is running!",
        "endpoints": {
            "POST /api/process": "Process grievance with AI",
            "POST /api/submit": "Submit grievance",
            "GET /api/grievances/<department>": "Get grievances",
            "GET /api/departments": "Get departments"
        }
    })


# ================= AI PROCESS ==================
@app.route('/api/process', methods=['POST'])
def process_grievance():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing grievance text"}), 400

        text = data["text"]

        structured = ai.structure_grievance(text)
        department = ai.classify_department(text)
        priority = ai.assign_priority(text)

        return jsonify({
            "success": True,
            "structured": structured,
            "department": department,
            "priority": priority
        })

    except Exception as e:
        print("Error /api/process:", e)
        return jsonify({"error": str(e)}), 500


# ================= SAVE TO DB ==================
@app.route('/api/submit', methods=['POST'])
def submit_grievance():
    try:
        data = request.get_json()

        required = ["name", "email", "original_text", "structured_text", "department", "priority"]
        for f in required:
            if f not in data:
                return jsonify({"error": f"Missing {f}"}), 400

        grievance_id = db.save_grievance(data)

        return jsonify({
            "success": True,
            "grievanceId": grievance_id
        })

    except Exception as e:
        print("Error /api/submit:", e)
        return jsonify({"error": str(e)}), 500


# ================= GET GRIEVANCES ==================
@app.route('/api/grievances/<department>', methods=['GET'])
def get_grievances(department):
    try:
        grievances = db.get_grievances_by_department(department)
        return jsonify({
            "success": True,
            "department": department,
            "count": len(grievances),
            "grievances": grievances
        })
    except Exception as e:
        print("Error /api/grievances:", e)
        return jsonify({"error": str(e)}), 500


# ================= DEPARTMENTS ==================
@app.route('/api/departments', methods=['GET'])
def get_departments():
    return jsonify({
        "success": True,
        "departments": db.get_all_departments()
    })

# ADD THIS NEW ENDPOINT HERE ⬇️⬇️⬇️
@app.route('/api/close', methods=['POST'])
def close_grievance():
    """
    Close a grievance with AI verification
    Expected input: {grievanceId, closureNotes}
    Returns: {approved, reason}
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'grievanceId' not in data or 'closureNotes' not in data:
            return jsonify({'error': 'Missing grievanceId or closureNotes'}), 400
        
        grievance_id = data['grievanceId']
        closure_notes = data['closureNotes']
        
        # Get the grievance from database
        grievance = db.get_grievance_by_id(grievance_id)
        
        if not grievance:
            return jsonify({'error': 'Grievance not found'}), 404
        
        # Verify closure with AI
        verification = ai.verify_closure(grievance['structuredText'], closure_notes)
        
        # Update database
        db.update_grievance_closure(grievance_id, closure_notes, verification['approved'])
        
        print(f"✅ Closure {'approved' if verification['approved'] else 'rejected'}: {grievance_id}")
        
        return jsonify({
            'success': True,
            'approved': verification['approved'],
            'reason': verification['reason'],
            'status': 'closed' if verification['approved'] else 'open'
        })
        
    except Exception as e:
        print(f"Error in /api/close: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ================= RUN ==================
if __name__ == "__main__":
    print("Grievance API Running on http://localhost:5000")
    app.run(debug=True, port=5000)
