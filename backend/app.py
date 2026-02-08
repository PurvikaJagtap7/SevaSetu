from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_service import (
    structure_grievance,
    classify_department,
    assign_priority,
    analyze_image,
    verify_closure
)
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import tempfile
from dotenv import load_dotenv
import random
from datetime import datetime
import json
from database import (
    init_db, create_user, authenticate_user, create_admin, authenticate_admin,
    save_grievance, get_grievances_by_user, get_grievances_by_department,
    get_grievance_by_id, update_grievance_status, get_all_grievances,
    get_departments, get_status_history, STATUS_STAGES
)

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# Initialize Twilio client
try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # Test the connection
    client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
    print("✅ Twilio client initialized and verified")
except Exception as e:
    print(f"❌ Twilio client initialization failed: {e}")
    client = None

# Store user conversation state
user_sessions = {}

# Initialize database
init_db()

# ------------------------
# API Routes
# ------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Nyaya Grievance Backend API",
        "time": datetime.now().isoformat(),
        "twilio_status": "configured" if client else "not configured",
        "endpoints": {
            "/process_grievance": "POST - Submit grievance",
            "/webhook/whatsapp": "POST - WhatsApp webhook",
            "/health": "GET - Health check",
            "/test_twilio": "GET - Test Twilio connection"
        }
    })

@app.route("/test_twilio", methods=["GET"])
def test_twilio():
    """Test endpoint to verify Twilio is working"""
    if not client:
        return jsonify({
            "status": "error",
            "message": "Twilio not configured. Check .env file."
        }), 500
    
    try:
        # Get account info
        account = client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
        return jsonify({
            "status": "success",
            "account_sid": account.sid,
            "account_status": account.status,
            "friendly_name": account.friendly_name,
            "message": "Twilio is configured correctly!"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/process_grievance", methods=["POST"])
def process_grievance():
    try:
        grievance_text = request.form.get("grievance_text") or request.form.get("grievance")
        phone_number = request.form.get("phone", "")
        
        if not grievance_text:
            return jsonify({
                "status": "error",
                "message": "Grievance text is required"
            }), 400

        location_data = {
            "city": request.form.get("city", ""),
            "state": request.form.get("state", ""),
            "area": request.form.get("area", ""),
            "place": request.form.get("place", ""),
            "pincode": request.form.get("pincode", ""),
            "specificLocation": request.form.get("specificLocation", "")
        }

        print(f"\n📝 Processing grievance:")
        print(f"   Text: {grievance_text[:50]}...")
        print(f"   Location: {location_data.get('city')}, {location_data.get('state')}")
        print(f"   Phone: {phone_number}")

        # -------------------------------
        # AI processing
        # -------------------------------
        structured = structure_grievance(grievance_text, location_data)
        department = classify_department(grievance_text, structured)
        priority = assign_priority(grievance_text, location_data)

        print(f"✅ AI Processing complete:")
        print(f"   Department: {department}")
        print(f"   Priority: {priority}")

        # -------------------------------
        # Image Handling
        # -------------------------------
        image_file = request.files.get("image")
        image_analysis = None
        if image_file:
            os.makedirs("uploads", exist_ok=True)
            # Unique filename
            image_path = f"uploads/{int(datetime.now().timestamp())}_{image_file.filename}"
            image_file.save(image_path)
            print(f"📷 Image saved: {image_path}")
            image_analysis = analyze_image(image_path, structured)

        grievance_id = f"GRV{random.randint(100000, 999999)}"

        # -------------------------------
        # WhatsApp Notification (Safe)
        # -------------------------------
        whatsapp_sent = False
        whatsapp_error = None

        try:
            phone_number = str(phone_number).strip()  # Force string

            if not phone_number:
                whatsapp_error = "Phone number missing"
                print("❌ WhatsApp not sent: phone number missing")
            else:
                import re
                clean_number = re.sub(r"[^\d+]", "", phone_number)

                # Add +91 fallback
                if not clean_number.startswith("+"):
                    if clean_number.startswith("91"):
                        clean_number = "+" + clean_number
                    else:
                        clean_number = "+91" + clean_number

                to_number = f"whatsapp:{clean_number}"

                location_parts = []
                if location_data.get('area'):
                    location_parts.append(location_data['area'])
                if location_data.get('place'):
                    location_parts.append(location_data['place'])
                if location_data.get('city'):
                    location_parts.append(location_data['city'])
                if location_data.get('state'):
                    location_parts.append(location_data['state'])
                location_str = ", ".join(location_parts) if location_parts else "Not specified"

                whatsapp_msg = f"""✅ *Grievance Registered Successfully*

🆔 *Grievance ID:* {grievance_id}

📝 *Summary:*
{structured[:400]}

🏢 *Department:* {department}
⚠️ *Priority:* {priority}

📍 *Location:*
{location_str}"""

                if image_analysis:
    # Safely include analysis as JSON string (first 200 chars)
                    analysis_text = json.dumps(image_analysis.get("analysis", {}))
                    whatsapp_msg += f"\n\n📷 *Image Analysis:*\n{analysis_text[:200]}"

                whatsapp_msg += "\n\n---\n💬 *Track your grievance:*\nSend your Grievance ID anytime to check status.\n\nThank you for using Nyaya! 🙏"

                print(f"📤 Sending WhatsApp to: {to_number}")
                print(f"📤 Message length: {len(whatsapp_msg)}")

                message = client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=to_number,
                    body=whatsapp_msg
                )

                whatsapp_sent = True
                print(f"✅ WhatsApp sent successfully! SID: {message.sid}, Status: {message.status}")

        except Exception as e:
            whatsapp_error = str(e)
            whatsapp_sent = False
            print(f"❌ WhatsApp sending failed: {whatsapp_error}")

        # -------------------------------
        # Save to Database
        # -------------------------------
        # Get user_id from session or create guest entry (user_id = None)
        user_id = request.form.get("user_id")  # Can be None for guest submissions
        
        image_path_value = None
        if image_file:
            image_path_value = image_path
        
        # Save grievance to database
        db_result = save_grievance(
            grievance_id=grievance_id,
            user_id=user_id if user_id else None,
            user_phone=phone_number,
            grievance_text=grievance_text,
            structured_text=structured,
            department=department,
            priority=priority,
            city=location_data.get('city'),
            state=location_data.get('state'),
            area=location_data.get('area'),
            place=location_data.get('place'),
            image_path=image_path_value,
            image_analysis=image_analysis,
            whatsapp_sent=whatsapp_sent
        )
        
        if not db_result.get("success"):
            print(f"⚠️ Database save warning: {db_result.get('error')}")
        
        print(f"✅ Grievance saved to database: {grievance_id} → {department}")

        # -------------------------------
        # Return JSON
        # -------------------------------
        return jsonify({
            "status": "success",
            "grievance_id": grievance_id,
            "structured": structured,
            "department": department,
            "priority": priority,
            "image_analysis": image_analysis,
            "whatsapp_sent": whatsapp_sent,
            "whatsapp_error": whatsapp_error,
            "phone_number": phone_number
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ------------------------
# WhatsApp Webhook - ENHANCED WITH MORE LOGGING
# ------------------------
@app.route("/webhook/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages"""
    
    # Log request headers
    print("\n" + "="*70)
    print(f"📱 WEBHOOK REQUEST RECEIVED - {datetime.now().isoformat()}")
    print("="*70)
    print(f"Method: {request.method}")
    print(f"Remote Addr: {request.remote_addr}")
    print(f"User Agent: {request.headers.get('User-Agent')}")
    
    # If GET request (testing)
    if request.method == "GET":
        print("⚠️  GET request (probably a test)")
        return jsonify({
            "status": "ok",
            "message": "Webhook is active and listening",
            "twilio_configured": client is not None,
            "time": datetime.now().isoformat()
        })
    
    try:
        # Log ALL form data
        print("\n📋 Complete Form Data:")
        for key, value in request.form.items():
            print(f"   {key}: {value}")
        
        # Extract Twilio parameters
        sender = request.form.get("From", "")
        body = request.form.get("Body", "").strip()
        media_url = request.form.get("MediaUrl0")
        num_media = int(request.form.get("NumMedia", 0))
        message_sid = request.form.get("MessageSid", "")
        
        print(f"\n📩 Extracted Data:")
        print(f"   From: {sender}")
        print(f"   Body: '{body}'")
        print(f"   Media URL: {media_url}")
        print(f"   Num Media: {num_media}")
        print(f"   Message SID: {message_sid}")
        
        # Create TwiML response
        resp = MessagingResponse()

        # Handle empty message
        if not body and num_media == 0:
            print("⚠️  Empty message - sending welcome")
            welcome_msg = """👋 *Welcome to Nyaya Grievance Portal!*

To submit a grievance:
1. Describe your issue
2. Optionally attach a photo

Example: "There is a pothole on MG Road"

How can I help you today?"""
            resp.message(welcome_msg)
            print(f"📤 Response: {welcome_msg[:50]}...")
            return str(resp), 200

        # Process the grievance
        print(f"\n🔄 Processing grievance from {sender}")
        
        location_data = {
            "city": "Mumbai",
            "state": "Maharashtra",
            "area": "",
            "place": "",
            "pincode": "",
            "specificLocation": body[:100]
        }

        try:
            print("🤖 Calling AI services...")
            
            structured = structure_grievance(body, location_data)
            print(f"✅ Structured: {structured[:100]}...")
            
            department = classify_department(body, structured)
            print(f"✅ Department: {department}")
            
            priority = assign_priority(body, location_data)
            print(f"✅ Priority: {priority}")
            
            image_analysis = None
            if media_url:
                print(f"📷 Processing image: {media_url}")
                try:
                    img_path = os.path.join(tempfile.gettempdir(), f"wa_{random.randint(1000,9999)}.jpg")
                    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    r = requests.get(media_url, auth=auth, timeout=10)
                    r.raise_for_status()
                    
                    with open(img_path, "wb") as f:
                        f.write(r.content)
                    
                    image_analysis = analyze_image(img_path, body)
                    print(f"✅ Image analyzed")
                except Exception as img_err:
                    print(f"❌ Image error: {img_err}")

            grievance_id = f"GRV{random.randint(100000, 999999)}"
            print(f"🆔 ID: {grievance_id}")

            success_msg = f"""✅ *Grievance Registered!*

🆔 *ID:* {grievance_id}

📝 *Summary:*
{structured[:300]}

🏢 *Department:* {department}
⚠️ *Priority:* {priority}"""

            if image_analysis:
                success_msg += f"\n\n📷 *Image:* {image_analysis[:100]}"

            success_msg += f"\n\n💬 Send *{grievance_id}* to check status."

            resp.message(success_msg)
            print(f"\n📤 Sending response ({len(success_msg)} chars)")
            print("="*70 + "\n")
            
            return str(resp), 200

        except Exception as process_err:
            print(f"❌ Processing error: {process_err}")
            import traceback
            traceback.print_exc()
            
            error_msg = "❌ Sorry, error processing your grievance. Please try again."
            resp.message(error_msg)
            return str(resp), 200

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        resp = MessagingResponse()
        resp.message("❌ System error. Please contact support.")
        return str(resp), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.now().isoformat(),
        "twilio_configured": client is not None,
        "account_sid": TWILIO_ACCOUNT_SID[:10] + "..." if TWILIO_ACCOUNT_SID else None
    })

# ------------------------
# Authentication Routes
# ------------------------

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """User signup"""
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        
        if not all([name, email, phone, password]):
            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400
        
        result = create_user(name, email, phone, password)
        
        if result.get("success"):
            return jsonify({
                "status": "success",
                "message": "User created successfully",
                "user_id": result.get("user_id")
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get("error")
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/auth/login", methods=["POST"])
def login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user_type = data.get("type", "user")  # "user" or "admin"
        
        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required"
            }), 400
        
        if user_type == "admin":
            result = authenticate_admin(email, password)
            if result.get("success"):
                return jsonify({
                    "status": "success",
                    "message": "Admin authenticated",
                    "user": result.get("admin"),
                    "type": "admin"
                })
        else:
            result = authenticate_user(email, password)
            if result.get("success"):
                return jsonify({
                    "status": "success",
                    "message": "User authenticated",
                    "user": result.get("user"),
                    "type": "user"
                })
        
        return jsonify({
            "status": "error",
            "message": result.get("error", "Invalid credentials")
        }), 401
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/auth/admin/signup", methods=["POST"])
def admin_signup():
    """Admin signup"""
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        department = data.get("department")
        
        if not all([name, email, password, department]):
            return jsonify({
                "status": "error",
                "message": "All fields are required"
            }), 400
        
        result = create_admin(name, email, password, department)
        
        if result.get("success"):
            return jsonify({
                "status": "success",
                "message": "Admin created successfully",
                "admin_id": result.get("admin_id")
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get("error")
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ------------------------
# Grievance Routes
# ------------------------

@app.route("/api/grievances/user/<int:user_id>", methods=["GET"])
def get_user_grievances(user_id):
    """Get all grievances for a user"""
    try:
        grievances = get_grievances_by_user(user_id)
        return jsonify({
            "status": "success",
            "grievances": grievances
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/grievances/department/<department>", methods=["GET"])
def get_department_grievances(department):
    """Get all grievances for a specific department"""
    try:
        grievances = get_grievances_by_department(department)
        return jsonify({
            "status": "success",
            "grievances": grievances
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/grievances/<grievance_id>", methods=["GET"])
def get_grievance(grievance_id):
    """Get a specific grievance by ID"""
    try:
        grievance = get_grievance_by_id(grievance_id)
        if grievance:
            return jsonify({
                "status": "success",
                "grievance": grievance
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Grievance not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/grievances/all", methods=["GET"])
def get_all_grievances_route():
    """Get all grievances (for super admin)"""
    try:
        grievances = get_all_grievances()
        return jsonify({
            "status": "success",
            "grievances": grievances
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/grievances/<grievance_id>/status", methods=["PUT"])
def update_grievance(grievance_id):
    """Update grievance status with WhatsApp notification"""
    print("\n" + "="*70)
    print(f"📊 STATUS UPDATE REQUEST for {grievance_id}")
    print("="*70)
    
    try:
        data = request.get_json()
        print(f"📥 Request data: {data}")
        
        status = data.get("status")
        note = data.get("note", "")
        admin_id = data.get("admin_id")
        
        print(f"   Status: {status}")
        print(f"   Note: {note[:50] if note else '(none)'}...")
        print(f"   Admin ID: {admin_id}")
        
        if not status:
            print("❌ ERROR: Status is required")
            return jsonify({
                "status": "error",
                "message": "Status is required"
            }), 400
        
        if status not in STATUS_STAGES:
            print(f"❌ ERROR: Invalid status '{status}'")
            return jsonify({
                "status": "error",
                "message": f"Invalid status. Must be one of: {', '.join(STATUS_STAGES)}"
            }), 400
        
        # Get grievance details for WhatsApp
        print(f"🔍 Fetching grievance {grievance_id}")
        grievance = get_grievance_by_id(grievance_id)
        if not grievance:
            print(f"❌ ERROR: Grievance {grievance_id} not found")
            return jsonify({
                "status": "error",
                "message": "Grievance not found"
            }), 404
        
        print(f"✅ Grievance found: {grievance.get('grievance_id')}")
        print(f"   Current status: {grievance.get('status')}")
        print(f"   User phone: {grievance.get('user_phone')}")
        
        # Update status
        print(f"💾 Updating status in database...")
        result = update_grievance_status(
            grievance_id, 
            status, 
            note=note,
            updated_by=admin_id,
            updated_by_type="admin"
        )
        
        if not result.get("success"):
            print(f"❌ ERROR: Database update failed: {result.get('error')}")
            return jsonify({
                "status": "error",
                "message": result.get("error", "Failed to update status")
            }), 500
        
        print(f"✅ Database updated successfully!")
        print(f"   {result.get('old_status')} → {result.get('new_status')}")
        
        # Send WhatsApp notification
        whatsapp_sent = False
        whatsapp_error = None
        
        if grievance.get("user_phone") and client:
            print(f"📱 Sending WhatsApp notification...")
            try:
                phone_number = str(grievance["user_phone"]).strip()
                import re
                clean_number = re.sub(r"[^\d+]", "", phone_number)
                
                if not clean_number.startswith("+"):
                    if clean_number.startswith("91"):
                        clean_number = "+" + clean_number
                    else:
                        clean_number = "+91" + clean_number
                
                to_number = f"whatsapp:{clean_number}"
                print(f"   To: {to_number}")
                
                # Create status update message
                status_msg = f"""📢 *Grievance Status Update*

🆔 *Grievance ID:* {grievance_id}

📊 *Status Changed:*
{result.get('old_status', 'Unknown')} → {status}

"""
                
                if note:
                    status_msg += f"📝 *Update Note:*\n{note}\n\n"
                
                status_msg += f"💬 *Track your grievance:*\nSend your Grievance ID to check latest status.\n\nThank you for using Nyaya! 🙏"
                
                message = client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=to_number,
                    body=status_msg
                )
                
                whatsapp_sent = True
                print(f"✅ WhatsApp sent! SID: {message.sid}")
                
            except Exception as e:
                whatsapp_error = str(e)
                print(f"❌ WhatsApp failed: {whatsapp_error}")
        else:
            if not grievance.get("user_phone"):
                print("⚠️ No phone number available")
            if not client:
                print("⚠️ Twilio client not configured")
        
        print("="*70)
        print(f"✅ STATUS UPDATE COMPLETE")
        print("="*70 + "\n")
        
        return jsonify({
            "status": "success",
            "message": "Grievance status updated",
            "whatsapp_sent": whatsapp_sent,
            "whatsapp_error": whatsapp_error
        })
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*70 + "\n")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ------------------------
# Department Routes
# ------------------------

@app.route("/api/departments", methods=["GET"])
def get_departments_route():
    """Get all departments"""
    try:
        departments = get_departments()
        return jsonify({
            "status": "success",
            "departments": departments
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/grievances/<grievance_id>/history", methods=["GET"])
def get_grievance_history(grievance_id):
    """Get status history for a grievance"""
    try:
        history = get_status_history(grievance_id)
        return jsonify({
            "status": "success",
            "history": history
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/status-stages", methods=["GET"])
def get_status_stages():
    """Get all available status stages"""
    return jsonify({
        "status": "success",
        "stages": STATUS_STAGES
    })

@app.route("/api/admin/profile/<int:admin_id>", methods=["GET"])
def get_admin_profile(admin_id):
    """Get admin profile with statistics"""
    try:
        from database import get_admin_profile_with_stats
        profile = get_admin_profile_with_stats(admin_id)
        
        if profile:
            return jsonify({
                "status": "success",
                "profile": profile
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Admin not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/dashboard/stats/<int:admin_id>", methods=["GET"])
def get_dashboard_stats(admin_id):
    """Get dashboard statistics for admin's department"""
    try:
        from database import get_admin_dashboard_stats
        stats = get_admin_dashboard_stats(admin_id)
        
        return jsonify({
            "status": "success",
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    print("\n" + "="*70)
    print("🚀 FLASK SERVER STARTING")
    print("="*70)
    print(f"🌐 Local: http://localhost:5000")
    print(f"📝 Grievance API: POST /process_grievance")
    print(f"📱 WhatsApp Webhook: POST /webhook/whatsapp")
    print(f"🔍 Test Twilio: GET /test_twilio")
    print(f"🔑 Twilio: {'✅ Configured' if client else '❌ Not Configured'}")
    if TWILIO_ACCOUNT_SID:
        print(f"🆔 SID: {TWILIO_ACCOUNT_SID[:10]}...")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000)