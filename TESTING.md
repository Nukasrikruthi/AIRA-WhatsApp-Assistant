# AIRA Testing Guide

## Overview

This document provides comprehensive testing guidelines for the AIRA WhatsApp Parent Assistant MVP.

## Test Levels

### 1. Unit Tests
Test individual functions and services in isolation.

### 2. Integration Tests
Test API endpoints with actual database.

### 3. End-to-End Tests
Test complete workflows through WhatsApp.

## Running Tests

### Setup Test Environment

```bash
# Navigate to project
cd "C:\Users\Home1\Documents\A Sria things\AIRA"

# Activate virtual environment
venv\Scripts\activate

# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

### Run Specific Test Class

```bash
pytest tests/test_api.py::TestParentAPI -v
```

### Run Specific Test

```bash
pytest tests/test_api.py::TestParentAPI::test_create_parent -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

## Test Cases

### Parent API Tests

#### 1. Create Parent
```
Input: 
  - phone_number: +6302894103
  - name: Rajesh Sharma
  - email: rajesh@email.com

Expected Output:
  - Status: 200
  - Response includes created parent with all details
```

#### 2. Get Parent by Phone
```
Input:
  - phone_number: +6302894103

Expected Output:
  - Status: 200
  - Returns parent information
  - Status: 404 if not found
```

#### 3. Get Parent Students
```
Input:
  - parent_id: 1

Expected Output:
  - Status: 200
  - Returns list of parent's students
  - Empty list if no students
```

### Student API Tests

#### 1. Get Student Profile
```
Input:
  - student_id: 1

Expected Output:
  - Status: 200
  - Includes student info, attendance, fees, marks, homework
  - Status: 404 if student not found
```

#### 2. Get Attendance Summary
```
Input:
  - student_id: 1

Expected Output:
  - Status: 200
  - attendance_percentage: 92
  - present_days: 120
  - absent_days: 8
  - leave_days: 2
  - total_days: 130
```

#### 3. Get Fee Status
```
Input:
  - student_id: 1

Expected Output:
  - Status: 200
  - total_fee: 60000
  - paid_fee: 55000
  - pending_fee: 5000
  - fee_percentage: 91.67
```

#### 4. Get Marks
```
Input:
  - student_id: 1

Expected Output:
  - Status: 200
  - average_percentage: 85.5
  - total_exams: 20
  - marks_by_subject: [...]
```

### WhatsApp Webhook Tests

#### 1. Message from Unregistered Parent
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+9999999999",
    "Body": "Hi",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: "Please contact admin for registration"
  - menu_state: "not_registered"
```

#### 2. Message from Registered Parent (Greeting)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "Hi",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Main menu with options
  - menu_state: "main"
```

#### 3. Select Student Profile (Option 1)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "1",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Student profile with:
    * Student name and class
    * Attendance percentage
    * Fee status
    * Marks average
    * Homework count
```

#### 4. View Attendance (Option 2)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "2",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Attendance summary
  - Recent attendance records
```

#### 5. View Fees (Option 3)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "3",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Fee summary with pending amounts
```

#### 6. View Marks (Option 4)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "4",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Marks summary with average
  - Recent exam results
```

#### 7. View Homework (Option 5)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "5",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Homework status
  - Pending assignments
```

#### 8. Back to Main Menu (Option 0)
```
Input:
  POST /api/whatsapp/webhook
  {
    "From": "whatsapp:+6302894103",
    "Body": "0",
    "MessageSid": "SM123..."
  }

Expected Output:
  - Status: 200
  - Response: Back to main menu
  - menu_state: "main"
```

## Manual Testing Workflow

### 1. Setup

```bash
# Terminal 1: Start the application
cd "C:\Users\Home1\Documents\A Sria things\AIRA"
venv\Scripts\activate
python scripts/seed_data.py  # Generate dummy data
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test APIs via Swagger

Open http://localhost:8000/docs

**Test Parent API:**
1. Click "Try it out" on GET /api/parents/{phone_number}
2. Enter phone_number: `+6302894103`
3. Click Execute
4. Should return parent details

**Test Student API:**
1. Click "Try it out" on GET /api/students/{student_id}/profile
2. Enter student_id: `1`
3. Click Execute
4. Should return complete profile

### 3. Test WhatsApp Webhook (Mock)

**Using Terminal/PowerShell:**

```powershell
# Test webhook with registered parent
$body = @{
    From = "whatsapp:+6302894103"
    Body = "Hi"
    MessageSid = "TEST123"
}

Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/webhook" `
  -Method POST `
  -Body $body

# Test webhook with unregistered parent
$body2 = @{
    From = "whatsapp:+9999999999"
    Body = "Hi"
    MessageSid = "TEST124"
}

Invoke-WebRequest -Uri "http://localhost:8000/api/whatsapp/webhook" `
  -Method POST `
  -Body $body2
```

### 4. Test with Twilio WhatsApp Sandbox (Real Testing)

#### Setup Twilio Account

1. Go to https://www.twilio.com/console
2. Get your Account SID and Auth Token
3. Go to Programmable Messaging → WhatsApp Sandbox Settings
4. Get sandbox phone number (e.g., +14155552671)

#### Configure .env

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
```

#### Setup Public URL (Ngrok)

```bash
# Download ngrok from https://ngrok.com
# Run:
ngrok http 8000

# Get URL like: https://xxxxxx.ngrok.io
```

#### Configure Webhook in Twilio

1. In Twilio Console → Programmable Messaging → Settings
2. Set Webhook URL to: `https://xxxxxx.ngrok.io/api/whatsapp/webhook`

#### Send Test WhatsApp Message

1. Add sandbox phone to your WhatsApp contacts
2. Send message: "join <sandbox-keyword>"
3. Then send: "Hi"
4. Parent should see welcome message with menu options

## Expected Test Results

### Summary Statistics

```
Tests Run: 25+
Expected Pass Rate: 95%+
Coverage Target: >80%

Critical Paths (100% coverage):
- WhatsApp message parsing
- Parent authentication
- Student data retrieval
- Session management
```

## Common Issues & Solutions

### Issue: Tests Fail with "Database locked"

**Solution:**
```bash
# Delete the test database
rm aira.db

# Recreate fresh
python scripts/seed_data.py
```

### Issue: Port 8000 Already in Use

**Solution:**
```bash
# Kill the process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Issue: Twilio Messages Not Received

**Solution:**
1. Check Twilio Account SID and Auth Token
2. Verify webhook URL is accessible (test with curl)
3. Check firewall/network settings
4. View Twilio logs for errors

### Issue: Session Not Persisting

**Solution:**
1. Ensure database is connected
2. Check ParentSession table in database
3. Verify session ID is being passed correctly

## Performance Benchmarks

### Expected Response Times

```
GET /api/parents/{phone}:          < 100ms
GET /api/students/{id}/profile:    < 200ms
GET /api/students/{id}/attendance: < 150ms
POST /api/whatsapp/webhook:        < 500ms (including Twilio call)
```

### Load Testing

```bash
pip install locust

# Create locustfile.py with load test scenarios
locust -f locustfile.py --host=http://localhost:8000
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=app
```

## Test Data Management

### Seeding Data

```bash
# Generate dummy data
python scripts/seed_data.py

# This creates:
# - 10 parents
# - 20 students
# - 130 attendance records per student
# - 12 fee records per student
# - 10 homework per student
# - 20 mark records per student
```

### Clearing Data

```python
from app.database.engine import SessionLocal
from app.models.models import *

db = SessionLocal()
db.query(Mark).delete()
db.query(Homework).delete()
db.query(Fee).delete()
db.query(Attendance).delete()
db.query(Student).delete()
db.query(Parent).delete()
db.query(Class).delete()
db.commit()
```

## Checklist Before Production

- [ ] All API tests passing
- [ ] All service tests passing
- [ ] Attendance calculation verified
- [ ] Fee calculation verified
- [ ] WhatsApp message formatting correct
- [ ] Session management working
- [ ] Error handling comprehensive
- [ ] Logging configured
- [ ] Database backups working
- [ ] Rate limiting configured (if needed)
- [ ] Security headers added
- [ ] HTTPS enabled (production)
- [ ] Twilio credentials secured
- [ ] Database encrypted (production)

---

For more information, see:
- [README.md](README.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database design
