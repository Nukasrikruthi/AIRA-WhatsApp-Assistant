# AIRA Deployment & Setup Guide

## Complete Setup Instructions

### Phase 1: Local Development Setup

#### 1. Clone/Navigate to Project

```bash
cd "C:\Users\Home1\Documents\A Sria things\AIRA"
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### 4. Setup Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit .env file with your settings
# (Open .env in VS Code and update values)
```

**Update these in .env:**
```env
# Database (default works for local)
DATABASE_URL=sqlite:///./aira.db

# Twilio - Get from https://www.twilio.com/console
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671

# FastAPI Settings
DEBUG=True
LOG_LEVEL=INFO
```

#### 5. Initialize Database

```bash
# Option A: Generate dummy data (recommended for MVP)
python scripts/seed_data.py

# This will:
# - Create all database tables
# - Generate 10 parents
# - Generate 20 students
# - Create attendance, fees, marks, homework records
```

#### 6. Run Application Locally

```bash
# Start the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

#### 7. Verify Installation

Open in browser:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **ReDoc:** http://localhost:8000/redoc

### Phase 2: Twilio Setup for WhatsApp

#### 1. Create Twilio Account

1. Go to https://www.twilio.com/try-twilio
2. Sign up and verify phone number
3. Get Account SID and Auth Token from Console
4. Add credit (free trial includes $15)

#### 2. Setup WhatsApp Sandbox

1. Go to Twilio Console → Messaging → Try it out → Send an SMS
2. Select WhatsApp from the messaging options
3. You'll see a Sandbox Number (e.g., +14155552671)
4. Get the Sandbox Keyword from the page

#### 3. Test Sandbox

1. Add the Twilio sandbox number to your WhatsApp contacts
2. Send WhatsApp message: `join <sandbox-keyword>`
   - Example: `join cozy-rainbow`
3. You should receive confirmation

#### 4. Configure Webhook URL

**Local Testing with Ngrok:**

```bash
# Download ngrok from https://ngrok.com/download
# Extract and run:

ngrok http 8000

# Copy the URL (example: https://abc123.ngrok.io)
```

**Update Twilio:**

1. Go to Twilio Console → Messaging → Settings
2. Find "Webhook" section
3. Enter: `https://your-ngrok-url/api/whatsapp/webhook`
4. Method: POST
5. Save

#### 5. Update .env with Twilio Credentials

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
```

#### 6. Test Message Flow

1. Restart FastAPI application
2. In WhatsApp, send to Twilio sandbox: "Hi"
3. You should receive menu response
4. Try options: 1, 2, 3, 4, 5

### Phase 3: Running Tests

#### 1. Install Test Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov
```

#### 2. Run All Tests

```bash
pytest tests/ -v

# Expected output:
# test_api.py::TestHealth::test_root_endpoint PASSED
# test_api.py::TestHealth::test_health_endpoint PASSED
# ... more tests ...
# ============= X passed in Y.XXs =============
```

#### 3. Run Specific Test Suite

```bash
# Test parents API
pytest tests/test_api.py::TestParentAPI -v

# Test students API
pytest tests/test_api.py::TestStudentAPI -v

# Test WhatsApp
pytest tests/test_api.py::TestWhatsAppWebhook -v
```

#### 4. Generate Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html

# Open htmlcov/index.html in browser to see coverage
```

### Phase 4: Project Structure Verification

After setup, your project should look like:

```
AIRA/
├── app/
│   ├── core/
│   │   ├── config.py          ✓ Configuration
│   │   └── __init__.py
│   ├── database/
│   │   ├── engine.py          ✓ Database setup
│   │   └── __init__.py
│   ├── models/
│   │   ├── models.py          ✓ ORM Models
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── schemas.py         ✓ Pydantic schemas
│   │   └── __init__.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── whatsapp.py    ✓ WhatsApp webhook
│   │   │   ├── parent.py      ✓ Parent endpoints
│   │   │   ├── student.py     ✓ Student endpoints
│   │   │   ├── attendance.py  ✓ Attendance endpoints
│   │   │   ├── fees.py        ✓ Fee endpoints
│   │   │   ├── marks.py       ✓ Marks endpoints
│   │   │   ├── homework.py    ✓ Homework endpoints
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── parent_service.py      ✓ Parent logic
│   │   ├── student_service.py     ✓ Student logic
│   │   ├── whatsapp_service.py    ✓ WhatsApp logic
│   │   └── __init__.py
│   ├── integrations/
│   │   ├── twilio_client.py   ✓ Twilio integration
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── test_api.py            ✓ API tests
│   └── __init__.py
├── scripts/
│   ├── seed_data.py           ✓ Data generation
│   └── __init__.py
├── logs/
│   └── (application logs)
├── main.py                    ✓ FastAPI app
├── requirements.txt           ✓ Dependencies
├── .env.example               ✓ Config template
├── .env                       ✓ Local config (not in git)
├── .gitignore                 ✓ Git ignore
├── README.md                  ✓ Quick start
├── ARCHITECTURE.md            ✓ System design
├── DATABASE_SCHEMA.md         ✓ Database design
├── TESTING.md                 ✓ Testing guide
├── DEPLOYMENT.md              ✓ This file
├── aira.db                    ✓ SQLite database (created after seed)
└── venv/                      ✓ Virtual environment
```

### Phase 5: Production Deployment

#### 1. Environment Setup

```bash
# Create production .env
cp .env.example .env.production

# Update with production values
# - Use PostgreSQL instead of SQLite
# - Use production Twilio settings
# - Set DEBUG=False
# - Use strong SECRET_KEY
```

#### 2. Database Migration (SQLite to PostgreSQL)

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Update DATABASE_URL in .env.production
DATABASE_URL=postgresql://user:password@localhost/aira_db
```

#### 3. Deploy to Cloud (Example: Heroku)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create aira-whatsapp-assistant

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_WHATSAPP_NUMBER=your_number
heroku config:set DEBUG=False

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

#### 4. Configure Production Webhook

1. Get your Heroku URL: `heroku apps:info -s | grep web_url`
2. In Twilio Console → Webhook URL: `https://your-heroku-app/api/whatsapp/webhook`
3. Update parent phone numbers in database with real Twilio numbers

### Phase 6: Monitoring & Maintenance

#### 1. Logging

```bash
# View application logs
tail -f logs/aira.log

# Or with timestamps
tail -f logs/aira.log | grep ERROR
```

#### 2. Database Backup

```bash
# Backup SQLite
sqlite3 aira.db ".backup aira_backup.db"

# Restore
sqlite3 aira.db ".restore aira_backup.db"

# PostgreSQL backup
pg_dump dbname > backup.sql

# Restore PostgreSQL
psql dbname < backup.sql
```

#### 3. Performance Monitoring

```bash
# Check API response times
curl -w "Time: %{time_total}s\n" http://localhost:8000/api/parents/+6302894103

# Monitor database size
ls -lh aira.db

# Check active connections
sqlite3 aira.db "PRAGMA database_list;"
```

### Phase 7: Troubleshooting

#### Issue: "Port 8000 already in use"

```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

#### Issue: "ModuleNotFoundError: No module named 'app'"

```bash
# Make sure you're in project root
cd "C:\Users\Home1\Documents\A Sria things\AIRA"

# And virtual environment is activated
venv\Scripts\activate
```

#### Issue: "Twilio messages not working"

```bash
# Check if credentials are set
python -c "from app.core.config import get_settings; s = get_settings(); print(f'SID: {s.twilio_account_sid}')"

# Test webhook health
curl http://localhost:8000/api/whatsapp/health

# Check Twilio logs in console
```

#### Issue: "Database locked"

```bash
# Close any open connections
# Delete and recreate database
rm aira.db
python scripts/seed_data.py
```

### Phase 8: Security Best Practices

#### 1. Secure Configuration

```python
# In production:
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]
CORS_ORIGINS = ["https://yourdomain.com"]
```

#### 2. Environment Variables

Never commit:
- `.env` file
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- Database passwords

Use environment variables or secrets management.

#### 3. Database Security

```bash
# Use strong credentials
DATABASE_URL=postgresql://strong_user:strong_password@secure_host/aira_db

# Enable SSL
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

#### 4. API Security

- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Rate limiting (future feature)
- ✅ CORS configured
- ✅ Error handling (no stack traces in production)

### Phase 9: Scaling for Production

#### 1. Load Balancing

```
Load Balancer (Nginx)
    ├── FastAPI Instance 1
    ├── FastAPI Instance 2
    └── FastAPI Instance N
        ↓
    PostgreSQL Database
        ↓
    Redis Cache
```

#### 2. Database Optimization

- Add indexes for frequently queried columns ✅
- Use connection pooling
- Regular backups (daily)
- Query optimization

#### 3. Caching Strategy

```bash
# Install Redis
pip install redis

# In services:
from redis import Redis
redis_client = Redis(host='localhost', port=6379)
```

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured
- [ ] Database initialized (`python scripts/seed_data.py`)
- [ ] Application running (`uvicorn main:app --reload`)
- [ ] Accessible at http://localhost:8000/docs
- [ ] Twilio account created and configured
- [ ] Webhook URL configured in Twilio
- [ ] Tests passing (`pytest tests/ -v`)
- [ ] Ready for development/testing

## Support & Documentation

- **Quick Start:** [README.md](README.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Database:** [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)
- **Testing:** [TESTING.md](TESTING.md)
- **Twilio Docs:** https://www.twilio.com/docs/whatsapp
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/

---

**Version:** 1.0.0 MVP
**Last Updated:** June 2024
**Status:** Ready for Development & Testing
