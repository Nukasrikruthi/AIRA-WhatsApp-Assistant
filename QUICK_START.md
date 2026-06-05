# AIRA - Quick Start Guide (5 Minutes)

Get AIRA running in 5 minutes!

## Prerequisites
- Windows 10/11 or macOS/Linux
- Python 3.8 or higher
- Git (optional)

## Step 1: Navigate to Project (30 seconds)

```bash
cd "C:\Users\Home1\Documents\A Sria things\AIRA"
```

## Step 2: Create Virtual Environment (1 minute)

```bash
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

## Step 4: Initialize Database (1 minute)

```bash
python scripts/seed_data.py
```

This creates:
- ✓ 10 parents with realistic phone numbers
- ✓ 20 students across classes 5-12
- ✓ 130 attendance records per student
- ✓ Monthly fee records
- ✓ Homework assignments
- ✓ Exam marks & grades

## Step 5: Run Application (30 seconds)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 6: Access API (30 seconds)

Open in your browser:

**Interactive API Docs:** http://localhost:8000/docs

**Health Check:** http://localhost:8000/health

## 🎉 You're Done!

Your AIRA API is now running!

---

## Next Steps

### Test API Endpoints

Go to http://localhost:8000/docs and:

1. Click on **GET /api/parents/{phone_number}**
2. Click "Try it out"
3. Enter: `+6302894103`
4. Click Execute
5. See parent details!

### Test Student Profile

1. Scroll to **GET /api/students/{student_id}/profile**
2. Click "Try it out"
3. Enter: `1`
4. Click Execute
5. See complete student data with attendance, fees, marks!

### Setup Twilio WhatsApp (Optional)

For real WhatsApp integration:

1. Create free Twilio account: https://www.twilio.com
2. Get credentials (SID, Token, Phone)
3. Update `.env` file with credentials
4. Download ngrok: https://ngrok.com
5. Run: `ngrok http 8000`
6. Configure webhook in Twilio console
7. Send WhatsApp message to Twilio sandbox number

For detailed setup, see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Sample Data Available

### Parent 1 (Test with this!)
- Phone: **+6302894103**
- Name: Rajesh Sharma
- Students: Rahul (Class 8), Priya (Class 5)

### Parent 2
- Phone: **+6312456789**
- Name: Priya Desai
- Students: Multiple

### All 10 Parents
See in browser or via API:
```bash
curl "http://localhost:8000/api/parents/+6302894103"
```

---

## Try These Requests

### Get Parent Info
```bash
curl "http://localhost:8000/api/parents/+6302894103"
```

### Get Student Profile
```bash
curl "http://localhost:8000/api/students/1/profile"
```

### Get Attendance
```bash
curl "http://localhost:8000/api/students/1/attendance"
```

### Get Fees
```bash
curl "http://localhost:8000/api/students/1/fees"
```

### Get Marks
```bash
curl "http://localhost:8000/api/students/1/marks"
```

### Get Homework
```bash
curl "http://localhost:8000/api/students/1/homework"
```

---

## File Structure Overview

```
AIRA/
├── app/
│   ├── core/        → Configuration
│   ├── database/    → Database setup
│   ├── models/      → Database models
│   ├── schemas/     → API schemas
│   ├── api/         → API routes
│   ├── services/    → Business logic
│   └── integrations/→ Twilio integration
├── scripts/
│   └── seed_data.py → Generate dummy data
├── tests/
│   └── test_api.py  → Test suite
├── main.py          → FastAPI app
├── requirements.txt → Dependencies
├── .env             → Configuration (create from .env.example)
├── README.md        → Full documentation
├── ARCHITECTURE.md  → System design
├── API_USAGE.md     → API examples
├── TESTING.md       → Testing guide
└── DEPLOYMENT.md    → Deployment guide
```

---

## Common Commands

### Start Application
```bash
uvicorn main:app --reload
```

### Run Tests
```bash
pytest tests/ -v
```

### Regenerate Database
```bash
python scripts/seed_data.py
```

### Stop Application
```
Press Ctrl+C
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Troubleshooting

### "Port 8000 already in use"
```bash
# Use different port
uvicorn main:app --port 8001
```

### "Module not found"
```bash
# Make sure venv is activated
venv\Scripts\activate
```

### "Database locked"
```bash
# Delete and recreate
del aira.db
python scripts/seed_data.py
```

---

## Full Documentation

- **README.md** - Complete setup & overview
- **ARCHITECTURE.md** - System architecture
- **DATABASE_SCHEMA.md** - Database design
- **API_USAGE.md** - API reference with examples
- **TESTING.md** - Testing guide
- **DEPLOYMENT.md** - Production deployment

---

## What's Included in This MVP?

✅ **Complete Backend**
- FastAPI application
- SQLite database
- 8 database models
- 40+ API endpoints

✅ **Business Logic**
- Parent authentication
- Student profile aggregation
- Attendance calculation
- Fee tracking
- Marks & homework management
- Session management

✅ **WhatsApp Integration**
- Twilio webhook receiver
- Message parsing
- Context-aware responses
- Multi-student support
- Menu-based interface

✅ **Testing**
- API tests
- Service tests
- Integration tests
- Mock data generation

✅ **Documentation**
- Architecture guide
- Database schema
- API usage guide
- Testing guidelines
- Deployment instructions

---

## Next Phase Features

🔄 **Phase 2+**
- OTP authentication
- Real ERP integration
- Payment gateway
- Meta WhatsApp API
- AI chatbot
- Voice bot
- RAG system
- Multilingual support
- Parent-teacher messaging
- Real-time notifications

---

## Support

### API Documentation
Interactive docs at: http://localhost:8000/docs

### Questions?
1. Check [README.md](README.md)
2. Check [ARCHITECTURE.md](ARCHITECTURE.md)
3. Check [API_USAGE.md](API_USAGE.md)
4. Check [TESTING.md](TESTING.md)

---

**Ready to develop?** Start from [README.md](README.md) for comprehensive documentation!

**Version:** 1.0.0 MVP  
**Status:** Ready to Use  
**Last Updated:** June 2024
