# Nyaya Grievance Portal - Complete Application Overview

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 16 (React 19) with Tailwind CSS
- **Backend**: Flask (Python) with SQLite database
- **AI Services**: Groq API (LLaMA models) for text and vision processing
- **Notifications**: Twilio WhatsApp API
- **Database**: SQLite with automatic migrations

---

## 📊 Database Structure

### Tables

1. **users** - Citizen accounts
   - id, name, email, phone, password_hash, created_at

2. **admins** - Department admin accounts
   - id, name, email, password_hash, department, created_at

3. **departments** - Government departments (10 departments)
   - id, name, description, created_at

4. **grievances** - All submitted grievances
   - id, grievance_id, user_id, user_phone, grievance_text, structured_text
   - department, priority, status, resolution_note
   - city, state, area, place, image_path, image_analysis
   - whatsapp_sent, created_at, updated_at

5. **status_history** - Complete timeline of status changes
   - id, grievance_id, old_status, new_status, note
   - updated_by, updated_by_type, created_at

### Status Stages (6 stages)
1. **Pending** - Initial status when submitted
2. **Under Review** - Admin reviewing the grievance
3. **In Process** - Work has started
4. **On Hold** - Temporarily paused
5. **Resolved** - Issue resolved
6. **Closed** - Officially closed

### Departments (10 departments)
1. Public Health Department
2. Water Supply & Sanitation Department
3. Electricity Department
4. Roads & Infrastructure Department
5. Municipal Corporation
6. Police Department
7. Education Department
8. Transport Department
9. Housing & Urban Development
10. Environment & Forest Department

---

## 🔄 Complete User Flows

### 👤 CITIZEN FLOW

#### 1. Registration & Login
- **Signup** (`/signup`): User creates account with name, email, phone, password
- **Login** (`/login`): User logs in with email/password
- **Auto-seeded accounts**: 3 sample users available (see TEST_CREDENTIALS.md)
- **Session**: User data stored in sessionStorage

#### 2. Submit Grievance (`/grievance`)
**Process:**
1. User fills form:
   - WhatsApp number (required)
   - Location (City, State, Place, Area)
   - Optional image upload
   - Grievance description (free text)

2. On submission:
   - Form data sent to `POST /process_grievance`
   - **AI Processing** (via Groq/LLaMA):
     - `structure_grievance()` - Converts informal text to structured format
     - `classify_department()` - Routes to correct department
     - `assign_priority()` - Sets priority (high/medium/low)
     - `analyze_image()` - Analyzes uploaded image if provided
   
3. Backend creates:
   - Unique grievance ID (GRV + 6 digits)
   - Saves to database with all details
   - Creates initial "Pending" status in history
   - Routes to specific department

4. WhatsApp Notification:
   - Sends confirmation to user's phone
   - Includes: Grievance ID, Department, Priority, Summary

5. User redirected to homepage (`/`)

#### 3. Track Grievances (`/track`)
- Lists all grievances submitted by logged-in user
- Shows: Grievance ID, Department, Status, Date
- Color-coded status badges
- Click to view details

#### 4. Grievance Details (`/track/[id]`)
- Full grievance information
- Current status with color coding
- **Status Timeline**: Complete history of all status changes
- Shows: Timestamp, Old status → New status, Admin notes
- Latest update note prominently displayed

---

### 👨‍💼 ADMIN FLOW

#### 1. Admin Login (`/login` - Admin tab)
- Admin logs in with email/password
- Auto-seeded: 10 admins (one per department)
- Session stored in sessionStorage
- Redirected to `/dashboard`

#### 2. Admin Dashboard (`/dashboard`)
- Overview of all grievances
- Charts showing:
  - Priority distribution (Pie chart)
  - Department breakdown (Bar chart)
  - Daily trends (Line chart)
- List of grievances with status
- Click to view individual grievance

#### 3. View Grievance (`/admin/grievance/[id]`)
**Left Panel - Grievance Info:**
- Grievance ID, Citizen details
- Department, Priority, Status
- Full description and structured summary
- Location details
- Resolution notes (if any)

**Right Panel - Status Update:**
- Current status display
- Dropdown to select new status
- Optional note field for updates
- Status history timeline
- Shows who updated and when

#### 4. Update Status
**Process:**
1. Admin selects new status from dropdown
2. Optionally adds a note
3. Clicks "Update Status"
4. Backend:
   - Updates grievance status in database
   - Creates entry in status_history
   - Sends WhatsApp notification to user
   - Notification includes: Status change, Update note

5. User receives WhatsApp:
   - "Status Changed: Old → New"
   - Update note (if provided)
   - Link to track grievance

---

## 🤖 AI Processing Pipeline

### When Grievance is Submitted:

1. **Structure Grievance** (`structure_grievance()`)
   - Input: Informal complaint text
   - Output: Structured professional report with:
     - Issue Summary
     - Detailed Description
     - Location Details
     - Impact Analysis
     - Urgency Indicators
     - Expected Resolution

2. **Classify Department** (`classify_department()`)
   - Input: Grievance text + structured text
   - Output: Exact department name from 10 available
   - Uses intelligent mapping for variations
   - Example: "water issue" → "Water Supply & Sanitation Department"

3. **Assign Priority** (`assign_priority()`)
   - Input: Grievance text + location
   - Output: high / medium / low
   - Considers: Safety risks, urgency, affected population

4. **Analyze Image** (`analyze_image()`)
   - Input: Uploaded image + grievance text
   - Output: Image analysis with:
     - Description of what's visible
     - Issue detected
     - Whether image matches grievance
     - Severity assessment
     - Safety concerns

**All AI processing uses Groq API with LLaMA models**

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User/Admin login
- `POST /api/auth/admin/signup` - Admin registration

### Grievances
- `POST /process_grievance` - Submit new grievance (with AI processing)
- `GET /api/grievances/user/<user_id>` - Get user's grievances
- `GET /api/grievances/department/<department>` - Get department's grievances
- `GET /api/grievances/<grievance_id>` - Get specific grievance
- `GET /api/grievances/all` - Get all grievances (super admin)
- `PUT /api/grievances/<grievance_id>/status` - Update status (with WhatsApp)
- `GET /api/grievances/<grievance_id>/history` - Get status history

### Departments & Status
- `GET /api/departments` - Get all departments
- `GET /api/status-stages` - Get all status stages

### WhatsApp
- `POST /webhook/whatsapp` - Receive WhatsApp messages
- `GET /test_twilio` - Test Twilio connection

### Health
- `GET /health` - Health check
- `GET /` - API info

---

## 📱 WhatsApp Integration

### Two-Way Communication

#### 1. Outbound (System → User)
- **Grievance Submission**: Confirmation with ID, department, priority
- **Status Updates**: Notification when admin changes status
- **Format**: Structured messages with emojis and clear information

#### 2. Inbound (User → System)
- Users can submit grievances via WhatsApp
- Send text message (optionally with image)
- System processes same way as web form
- Responds with grievance ID and details

---

## 🎨 Frontend Pages

### Public Pages
- `/` - Landing page (features, hero section)
- `/about` - About the platform
- `/login` - Login (Citizen/Admin toggle)
- `/signup` - User registration

### Citizen Pages (After Login)
- `/citizen` - Citizen home (Submit/Track options)
- `/grievance` - Submit new grievance form
- `/track` - List of user's grievances
- `/track/[id]` - Grievance details with timeline
- `/profile` - User profile

### Admin Pages (After Login)
- `/dashboard` - Admin dashboard with charts
- `/admin/grievance/[id]` - Grievance detail with status update
- `/admin/profile` - Admin profile

---

## 🔐 Security & Authentication

- **Password Hashing**: Werkzeug (bcrypt-based)
- **Session Management**: sessionStorage (frontend)
- **CORS**: Enabled for frontend-backend communication
- **Input Validation**: Both frontend and backend
- **SQL Injection Protection**: Parameterized queries

---

## 🚀 Startup Process

### Backend (Flask)
1. Loads environment variables (.env)
2. Initializes Twilio client
3. Initializes database (creates tables if needed)
4. Seeds sample users and admins
5. Starts Flask server on port 5000

### Frontend (Next.js)
1. Runs on port 3000 (default)
2. Connects to backend at `http://localhost:5000`
3. All API calls use this base URL

---

## 📋 Complete Workflow Example

### Scenario: User Reports Water Leakage

1. **User Action**: 
   - Logs in → Goes to `/grievance`
   - Fills form: "Water leaking on MG Road for 3 days"
   - Uploads photo
   - Submits

2. **Backend Processing**:
   - Receives form data
   - AI structures: "Water Supply Issue - MG Road - 3 days duration"
   - AI classifies: "Water Supply & Sanitation Department"
   - AI assigns: "high" priority (safety concern)
   - AI analyzes image: "Water leakage visible, matches description"
   - Generates ID: GRV123456
   - Saves to database
   - Routes to Water Supply department

3. **Notifications**:
   - WhatsApp sent to user: "Grievance Registered - ID: GRV123456 - Department: Water Supply..."

4. **Admin Action**:
   - Water Supply admin logs in
   - Sees grievance in dashboard
   - Opens detail page
   - Updates status: "Pending" → "In Process"
   - Adds note: "Team dispatched, repair scheduled for tomorrow"

5. **User Notification**:
   - WhatsApp: "Status Update - Pending → In Process - Team dispatched..."

6. **User Tracking**:
   - User goes to `/track`
   - Sees grievance with "In Process" status
   - Clicks to view details
   - Sees complete timeline with admin note

7. **Resolution**:
   - Admin updates: "In Process" → "Resolved"
   - Note: "Leakage fixed on Jan 25, 2026. Work order #WS-445"
   - User receives WhatsApp notification
   - User sees "Resolved" status in tracking

---

## 🎯 Key Features

✅ **AI-Powered Processing**: Automatic department routing and priority assignment
✅ **Multi-Channel Submission**: Web form + WhatsApp
✅ **Real-Time Tracking**: Status updates with complete history
✅ **WhatsApp Notifications**: Automatic updates on status changes
✅ **Department Routing**: Automatic assignment to correct department
✅ **Image Analysis**: AI verifies uploaded images match grievance
✅ **Status Timeline**: Complete audit trail of all changes
✅ **Admin Notes**: Context for each status update
✅ **Color-Coded Status**: Visual indicators throughout
✅ **Auto-Seeded Data**: Test accounts ready on startup

---

## 📝 Environment Variables Required

```env
# Twilio (for WhatsApp)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Groq (for AI)
GROQ_API_KEY=your_groq_api_key
```

---

## 🧪 Testing

### Sample Accounts (Auto-created)
- **Users**: See `backend/TEST_CREDENTIALS.md`
- **Admins**: See `backend/TEST_CREDENTIALS.md`
- All passwords: `password123` (users) / `admin123` (admins)

### Test Flow
1. Start backend: `python backend/app.py`
2. Start frontend: `npm run dev` (in frontend folder)
3. Login as user → Submit grievance → Check tracking
4. Login as admin → View grievance → Update status
5. Check WhatsApp notifications

---

## 🔧 File Structure

```
SevaSetu/
├── backend/
│   ├── app.py              # Flask API server
│   ├── database.py         # Database models & functions
│   ├── ai_service.py       # AI processing (Groq)
│   ├── requirements.txt    # Python dependencies
│   ├── TEST_CREDENTIALS.md # Test account info
│   └── uploads/            # Uploaded images
│
├── frontend/
│   ├── app/
│   │   ├── page.jsx        # Landing page
│   │   ├── login/          # Login page
│   │   ├── signup/         # Signup page
│   │   ├── citizen/        # Citizen home
│   │   ├── grievance/      # Submit grievance
│   │   ├── track/          # Track grievances
│   │   ├── dashboard/      # Admin dashboard
│   │   ├── admin/          # Admin pages
│   │   └── components/     # Reusable components
│   └── package.json
│
└── grievance_db.sqlite     # SQLite database (auto-created)
```

---

## 🎓 Summary

**Nyaya Grievance Portal** is a complete AI-powered public grievance redressal system that:
- Allows citizens to submit complaints in simple language
- Uses AI to route to correct departments automatically
- Enables admins to track and update grievance status
- Sends real-time WhatsApp notifications
- Provides complete transparency with status tracking
- Supports both web and WhatsApp submission channels

The system is production-ready with authentication, database persistence, AI processing, and multi-channel communication.

