from flask import Flask, render_template, request, jsonify
from ai_service import structure_grievance, classify_department, assign_priority, analyze_image, verify_closure

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_grievance", methods=["POST"])
def process_grievance():
    # Text grievance
    grievance_text = request.form.get("grievance_text")
    
    # Optional location
    location_data = {
        "city": request.form.get("city", ""),
        "area": request.form.get("area", ""),
        "pincode": request.form.get("pincode", ""),
        "specificLocation": request.form.get("specificLocation", "")
    }
    
    
    
    # Run AI functions
    structured = structure_grievance(grievance_text, location_data)
    department = classify_department(grievance_text, structured)
    priority = assign_priority(grievance_text, location_data)
    
    # File upload
    image_file = request.files.get("image")
    image_analysis = None
    if image_file:
        image_path = f"uploads/{image_file.filename}"
        image_file.save(image_path)
        image_analysis = analyze_image(image_path,structured)
    return jsonify({
        "structured_grievance": structured,
        "department": department,
        "priority": priority,
        "image_analysis": image_analysis
    })

if __name__ == "__main__":
    import os
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
