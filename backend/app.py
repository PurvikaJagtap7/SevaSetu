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
