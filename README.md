# ⚖️ Nyaya Grievance Portal — AI-Powered Public Grievance Redressal System

Nyaya Grievance Portal is an AI-powered, multi-channel grievance redressal platform that enables citizens to submit complaints easily and ensures automatic routing, priority detection, real-time tracking, and transparent resolution workflows.

The system combines AI processing, WhatsApp integration, analytics dashboards, and department-based administration to make grievance handling more accessible, efficient, and transparent.

---

# 🚀 Features

- 🤖 AI-powered grievance processing
- 🏢 Automatic department routing
- 🎯 AI-based priority assignment
- 📝 Text structuring of informal complaints
- 🖼 Image verification using AI vision models
- 📱 Dual submission channels — Web + WhatsApp
- 🔔 Real-time WhatsApp notifications
- 📊 Admin analytics dashboards
- 🧾 Complete audit trail
- 🔐 Secure authentication
- ⚡ Fast processing (2–5 seconds per grievance)

---

# 🧠 AI Intelligent Processing

The portal uses **Groq AI (LLaMA models)** to automatically process grievances with four AI functions:

1. Text Structuring — Converts raw complaints into professional reports  
2. Department Classification — Routes to correct department  
3. Priority Detection — Assigns High / Medium / Low priority  
4. Image Analysis — Validates uploaded images with complaint context  

### Example

User input:
> “Water leaking on MG Road for 3 days”

System output:
- Structured report generated
- Routed to Water Supply Department
- Priority set to High

No manual classification required.

---

# 📱 Multi-Channel Submission

## 🌐 Web Portal
- Complaint form
- Image upload
- Structured submission
- Tracking dashboard

## 💬 WhatsApp
- Submit via message
- Optional image upload
- Instant confirmation
- Status updates via WhatsApp

No app download required — improves accessibility.

---

# 🎯 Status Workflow

Each grievance moves through defined stages:
Pending → Under Review → In Process → On Hold → Resolved → Closed


### Transparency Includes

- Status timeline
- Admin name recorded
- Timestamp logging
- Admin notes
- Previous → new status tracking
- WhatsApp alerts on updates

---

# 🏢 Supported Departments

- Public Health
- Water Supply & Sanitation
- Electricity
- Roads & Infrastructure
- Municipal Corporation
- Police
- Education
- Transport
- Housing & Urban Development
- Environment & Forest

Each department has its own admin dashboard and filtered grievance view.

---

# 📊 Admin Analytics

Real-time dashboards include:

- Priority distribution (pie chart)
- Department comparison (bar chart)
- Daily grievance trends (7-day line chart)

Metrics shown:
- Total grievances
- Resolved cases
- Pending cases
- Status breakdown
- Department performance

---

# ⚙️ Workflow Automation

Automated pipeline:

1. Citizen submits complaint
2. AI processes text & image
3. Department auto-selected
4. Priority auto-assigned
5. WhatsApp confirmation sent
6. Admin updates status
7. User notified instantly
8. Audit trail stored

### Processing Time

| System | Time |
|---------|--------|
Traditional | 15–20 min |
Nyaya Portal | **2–5 sec** |

---

# 🎨 UI Features

- Clean, simple interface
- Responsive design
- Color-coded status badges
- Real-time updates
- Accessibility-friendly language

Status Colors:

- Pending — Gray
- Under Review — Yellow
- In Process — Blue
- On Hold — Orange
- Resolved — Green
- Closed — Dark Gray

---

# 🏗 Tech Stack

## Frontend
- Next.js 16
- React 19

## Backend
- Flask (Python)

## Database
- SQLite

## AI
- Groq API
- LLaMA models
- Vision models

## Messaging
- Twilio WhatsApp API

---

# 🔐 Security

- Password hashing (bcrypt)
- Parameterized SQL queries
- SQL injection protection
- Input validation
- Secure API endpoints
- CORS configured

---

# 📈 Performance & Scalability

- Handles 1000+ grievances
- Optimized queries
- <500ms average API response
- Modular architecture
- Production-ready design

---



# 📄 License

This project is for academic / demonstration use. Add your preferred license if deploying publicly.

