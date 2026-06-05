# AIRA - WhatsApp Parent Assistant MVP

**A complete WhatsApp-based Parent Assistant integrated with School ERP system**

## 📋 Overview

AIRA (AI-powered Remote Assistant) is an enterprise-grade MVP that connects parents with their child's school information via WhatsApp. Parents can instantly access:

- Student Profile & Academic Performance
- Real-time Attendance Records
- Fee Status & Due Dates
- Homework Assignments
- Exam Marks & Grades

## 🏗️ Architecture

### Project Structure

```
AIRA/
├── app/
│   ├── core/                 # Core configuration
│   │   ├── config.py        # Settings management
│   │   └── __init__.py
│   ├── database/             # Database setup
│   │   ├── engine.py        # SQLAlchemy engine & session
│   │   └── __init__.py
│   ├── models/               # Database models
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   └── __init__.py
│   ├── schemas/              # Pydantic schemas
│   │   ├── schemas.py       # Request/Response validators
│   │   └── __init__.py
│   ├── api/                  # API routes
│   │   ├── routes/
│   │   │   ├── parent.py    # Parent APIs
│   │   │   ├── student.py   # Student APIs
│   │   │   ├── attendance.py # Attendance APIs
│   │   │   ├── fees.py      # Fee APIs
│   │   │   ├── homework.py  # Homework APIs
│   │   │   ├── marks.py     # Marks APIs
│   │   │   ├── whatsapp.py  # WhatsApp webhook
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/             # Business logic
│   │   ├── parent_service.py # Parent operations
│   │   ├── student_service.py # Student operations
│   │   ├── whatsapp_service.py # WhatsApp logic
│   │   └── __init__.py
│   ├── integrations/         # External integrations
│   │   ├── twilio_client.py # Twilio WhatsApp
│   │   └── __init__.py
│   └── __init__.py
├── tests/                    # Test suite
│   ├── test_api.py
│   ├── test_services.py
│   └── __init__.py
├── logs/                     # Application logs
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore patterns
└── README.md                # This file
```

### Database Schema

**Entities:**
- `Parent` - Parent information with WhatsApp phone number
- `Class` - School classes (Class 1-12)
- `Student` - Student information linked to parents
- `Attendance` - Daily attendance records
- `Fee` - Monthly fee records with payment status
- `Homework` - Homework assignments per student
- `Mark` - Exam results and marks
- `ParentSession` - Session management for WhatsApp conversations

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | FastAPI 0.104.1 |
| Web Server | Uvicorn 0.24.0 |
| Database | SQLite (MVP) / PostgreSQL (Production) |
| ORM | SQLAlchemy 2.0.23 |
| Data Validation | Pydantic 2.5.0 |
| WhatsApp API | Twilio 8.10.0 |
| Testing | Pytest 7.4.3 |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Twilio Account (for WhatsApp Sandbox)

### Installation

1. **Clone and navigate to project:**
   ```bash
   cd "C:\Users\Home1\Documents\A Sria things\AIRA"
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Twilio credentials
   ```

5. **Initialize database:**
   ```bash
   python -c "from app.database.engine import engine; from app.models.models import Base; Base.metadata.create_all(bind=engine)"
   ```

6. **Seed dummy data:**
   ```bash
   python scripts/seed_data.py
   ```

7. **Run application:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Access API: http://localhost:8000
   Docs: http://localhost:8000/docs

## 📱 WhatsApp Conversation Flow

### User Interaction Example

```
Parent: "Hi"

Bot: "Welcome to AIRA Parent Assistant! 👋
     
     Please select an option:
     
     1️⃣ Student Profile
     2️⃣ Attendance
     3️⃣ Fee Details
     4️⃣ Marks
     5️⃣ Homework"

Parent: "1"

Bot: "Select Student:
     1️⃣ Rahul (Class 8)
     2️⃣ Priya (Class 5)"

Parent: "1"

Bot: "📚 RAHUL - Student Profile
     
     Class: 8A
     Roll Number: 008
     
     📊 ATTENDANCE: 92%
     Present: 120/130 days
     
     💰 FEE STATUS: Pending
     Due: ₹5,000
     Due Date: 15-Jan-2024
     
     📈 MARKS: 85%
     Average: 85%
     
     📝 PENDING HOMEWORK: 3
     
     Reply with:
     2️⃣ Detailed Attendance
     3️⃣ Detailed Fees
     4️⃣ Marks Details
     5️⃣ Homework Details"
```

## 🔌 API Endpoints

### Parent Endpoints
- `GET /api/parents/{phone_number}` - Get parent by phone
- `GET /api/parents/{parent_id}/students` - Get parent's students
- `POST /api/parents` - Create parent (admin)

### Student Endpoints
- `GET /api/students/{student_id}` - Get student profile
- `GET /api/students/{student_id}/profile` - Get comprehensive profile
- `GET /api/students/{student_id}/attendance` - Get attendance summary
- `GET /api/students/{student_id}/fees` - Get fee details
- `GET /api/students/{student_id}/marks` - Get marks
- `GET /api/students/{student_id}/homework` - Get homework

### WhatsApp Endpoints
- `POST /api/whatsapp/webhook` - Twilio webhook receiver
- `POST /api/whatsapp/send` - Send WhatsApp message (admin)

## 📊 Dummy Data

### Sample Data Structure

**10 Parents** with realistic WhatsApp numbers
**20 Students** across classes 5-12
**Attendance Records** - Monthly data for all students
**Fee Records** - Monthly fees with various statuses
**Homework** - 3-5 assignments per student
**Marks** - Unit tests, mid-term, finals for all students

See `scripts/seed_data.py` for detailed data generation.

## 🛠️ Development Phases

### Phase 1: Architecture & Database Design ✅
- Project structure
- Database schema
- Configuration management

### Phase 2: Database & Models ⏳
- SQLAlchemy models
- Pydantic schemas
- Dummy data generation

### Phase 3: FastAPI APIs ⏳
- CRUD endpoints
- Business logic services
- Error handling

### Phase 4: Twilio Integration ⏳
- WhatsApp webhook
- Message handling
- Session management

### Phase 5: Testing & Deployment ⏳
- Unit tests
- Integration tests
- Production readiness

## 🔐 Security Considerations

For MVP:
- ✅ Phone number-based parent identification
- ✅ Student data scoped to parent
- ⏳ OTP authentication (Phase 2+)
- ⏳ Role-based access control
- ⏳ Encryption for sensitive data

## 📈 Future Roadmap

### Phase 2 Enhancements
- [ ] OTP-based authentication
- [ ] Real ERP integration
- [ ] Payment gateway integration
- [ ] Bulk message notifications

### Phase 3 Advanced Features
- [ ] Meta WhatsApp API integration
- [ ] AI chatbot responses
- [ ] Voice message support
- [ ] Document sharing (marksheets, receipts)

### Phase 4 Enterprise Features
- [ ] Multi-school support
- [ ] Parent-Teacher messaging
- [ ] Event notifications
- [ ] Real-time alerts
- [ ] Analytics dashboard

### Phase 5 AI & ML
- [ ] RAG (Retrieval Augmented Generation)
- [ ] Natural language understanding
- [ ] Predictive analytics
- [ ] Multilingual support
- [ ] Voice bot

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 📝 Configuration

All settings are managed via `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./aira.db

# Twilio
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671

# FastAPI
DEBUG=True
LOG_LEVEL=INFO

# Session
SESSION_TIMEOUT=3600
```

## 🔄 Twilio WhatsApp Sandbox Setup

1. Go to Twilio Console → Programmable Messaging → Settings
2. Get your sandbox number: `whatsapp:+14155552671`
3. Send message: "join <sandbox-keyword>" to +1-415-523-8886
4. Update `.env` with Account SID and Auth Token
5. Configure webhook URL: `https://your-domain/api/whatsapp/webhook`

## 📚 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Support

For issues or questions, create an issue in the repository or contact the development team.

## 📄 License

This project is proprietary and confidential for now.

---

**Version:** 1.0.0 MVP  
**Last Updated:** June 2024  
**Status:** Under Active Development
