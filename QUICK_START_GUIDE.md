# Quick Start Guide - SevaSetu Grievance Portal

## Prerequisites
- Python 3.x installed
- Node.js and npm installed
- Twilio account credentials (optional for WhatsApp)

## Setup Instructions

### 1. Backend Setup (Flask)

```bash
# Navigate to backend directory
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Create .env file with Twilio credentials
# Create a file named .env in the backend folder with:
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Start Flask server
python app.py
```

The server will start on `http://localhost:5000`

Database will be automatically initialized with sample data on first run.

### 2. Frontend Setup (Next.js)

```bash
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## Testing the System

### Option 1: Use Sample Admin Credentials

Login as an admin at `http://localhost:3000/login`:
- **Email:** admin.health@example.com
- **Password:** admin123
- **Account Type:** Select "Admin"

Other admin accounts:
- admin.water@example.com (Water Supply Department)
- admin.electricity@example.com (Electricity Department)
- admin.infrastructure@example.com (Infrastructure Department)

### Option 2: Test User Account

Login as a citizen at `http://localhost:3000/login`:
- **Email:** sushmitasahu2710@gmail.com
- **Password:** susmita@123
- **Account Type:** Select "User/Citizen"

Or use:
- ramesh@example.com / password123
- priya@example.com / password123

### Submit a Grievance

1. Login as a citizen
2. Go to "Submit Grievance"
3. Fill in the form:
   - WhatsApp Number: +91XXXXXXXXXX
   - Location: City, State
   - Optional: Upload image
   - Describe your grievance
4. Click "Process Grievance"

The system will:
- Use AI to structure and classify the grievance
- Assign it to the appropriate department
- Determine priority level
- Send WhatsApp notification (if Twilio configured)
- Save to database

### View as Admin

1. Login as an admin (use department-specific admin account)
2. Go to "Dashboard" to see:
   - Priority distribution chart
   - Department comparison chart
   - Daily trend chart
   - Recent grievances from your department
3. Click "View" on any grievance to see full details
4. Update the status and add notes
5. WhatsApp notification will be sent to the user

### View Admin Profile

1. Login as admin
2. Click on "Profile" in navigation
3. See your admin details and statistics:
   - Total grievances handled
   - Resolved count
   - Pending count

## API Testing

To test the backend APIs directly:

```bash
cd backend
python test_admin_apis.py
```

This will test:
- Admin profile API
- Dashboard statistics API
- Grievances by department API
- All grievances API

## Features Verified

✅ **User Features:**
- Grievance submission with AI processing
- WhatsApp notifications
- Image upload and analysis
- Status tracking

✅ **Admin Features:**
- Department-specific dashboard
- Real-time statistics and charts
- Grievance detail view
- Status updates with notifications
- Profile with statistics

## Troubleshooting

### Backend not starting?
- Check if port 5000 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if Python version is compatible (Python 3.8+)

### Frontend not starting?
- Check if port 3000 is available
- Ensure all dependencies are installed: `npm install`
- Check if Node.js version is compatible (Node 16+)

### Grievances not showing?
- Ensure backend is running
- Check browser console for errors
- Verify you're logged in as admin
- Check that grievances exist for that department

### WhatsApp not working?
- This is optional - system works without it
- Verify Twilio credentials in .env file
- Check if Twilio sandbox is active
- Test with: `curl http://localhost:5000/test_twilio`

### Database issues?
- Delete `backend/grievance_db.sqlite` and restart Flask
- Database will be recreated with sample data

## Architecture Overview

```
User Submits Grievance
    ↓
Next.js Frontend (Port 3000)
    ↓
Flask Backend (Port 5000)
    ↓
AI Processing (OpenAI)
    ↓
SQLite Database
    ↓
Twilio WhatsApp API
    ↓
Notifications Sent
```

## Important URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **API Health Check:** http://localhost:5000/health
- **Twilio Test:** http://localhost:5000/test_twilio

## Key Files

**Backend:**
- `backend/app.py` - Main Flask application
- `backend/database.py` - Database operations
- `backend/ai_service.py` - AI processing
- `backend/grievance_db.sqlite` - SQLite database

**Frontend:**
- `frontend/app/grievance/page.jsx` - Grievance submission form
- `frontend/app/dashboard/page.jsx` - Admin dashboard
- `frontend/app/admin/profile/page.jsx` - Admin profile
- `frontend/app/admin/grievance/[id]/` - Grievance detail view

## Support

For issues or questions:
1. Check the IMPLEMENTATION_SUMMARY.md for detailed technical information
2. Check TEST_CREDENTIALS.md for all sample login credentials
3. Review backend/test_admin_apis.py for API examples

---

**System Status:** ✅ Fully Operational
**Last Updated:** January 24, 2026

