from flask import Flask, request, jsonify, render_template
from ai_service import structure_grievance, classify_department, assign_priority

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_grievance():
    data = request.json
    informal_text = data.get('grievance')
    
    location_data = {
        'city': data.get('city'),
        'area': data.get('area'),
        'pincode': data.get('pincode'),
        'specificLocation': data.get('specificLocation')
    }
    
    try:
        structured = structure_grievance(informal_text, location_data)
        department = classify_department(informal_text, structured)
        priority = assign_priority(informal_text, location_data)
        
        return jsonify({
            'structured': structured,
            'department': department,
            'priority': priority
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
