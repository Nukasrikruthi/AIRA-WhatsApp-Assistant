# AIRA API Usage Guide

## Getting Started

### Base URL
```
http://localhost:8000  (Development)
https://api.yourserver.com  (Production)
```

### Authentication
For MVP: Phone number-based identification

For Future: OAuth2 / API Keys

## API Endpoints Reference

### 1. Parent Endpoints

#### Create Parent
```
POST /api/parents/
Content-Type: application/x-www-form-urlencoded

Parameters:
- phone_number: string (required) - Format: +6302894103
- name: string (required)
- email: string (optional)
- alternate_phone: string (optional)

Example:
curl -X POST "http://localhost:8000/api/parents/" \
  -d "phone_number=%2B6302894103&name=Rajesh%20Sharma&email=rajesh@email.com"

Response: 200 OK
{
  "id": 1,
  "phone_number": "+6302894103",
  "name": "Rajesh Sharma",
  "email": "rajesh@email.com",
  "alternate_phone": null,
  "is_active": true,
  "created_at": "2024-01-10T10:30:00Z"
}
```

#### Get Parent by Phone
```
GET /api/parents/{phone_number}

Parameters:
- phone_number: string - Format: +6302894103

Example:
curl "http://localhost:8000/api/parents/%2B6302894103"

Response: 200 OK
{
  "id": 1,
  "phone_number": "+6302894103",
  "name": "Rajesh Sharma",
  "email": "rajesh@email.com",
  "is_active": true,
  "created_at": "2024-01-10T10:30:00Z"
}
```

#### Get Parent's Students
```
GET /api/parents/{parent_id}/students

Parameters:
- parent_id: integer

Example:
curl "http://localhost:8000/api/parents/1/students"

Response: 200 OK
[
  {
    "id": 1,
    "name": "Rahul",
    "roll_number": "001",
    "parent_id": 1,
    "class_id": 1,
    "email": "rahul@school.com",
    "is_active": true,
    "created_at": "2024-01-10T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Priya",
    "roll_number": "002",
    "parent_id": 1,
    "class_id": 2,
    "email": "priya@school.com",
    "is_active": true,
    "created_at": "2024-01-10T10:30:00Z"
  }
]
```

---

### 2. Student Endpoints

#### Get Student Details
```
GET /api/students/{student_id}

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1"

Response: 200 OK
{
  "id": 1,
  "name": "Rahul",
  "roll_number": "001",
  "parent_id": 1,
  "class_id": 1,
  "email": "rahul@school.com",
  "is_active": true,
  "created_at": "2024-01-10T10:30:00Z",
  "class_obj": {
    "id": 1,
    "name": "8",
    "created_at": "2024-01-10T10:30:00Z"
  }
}
```

#### Get Comprehensive Student Profile
```
GET /api/students/{student_id}/profile

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1/profile"

Response: 200 OK
{
  "student": {
    "id": 1,
    "name": "Rahul",
    "roll_number": "001",
    "class": "8",
    "email": "rahul@school.com"
  },
  "attendance": {
    "total_days": 130,
    "present_days": 120,
    "absent_days": 8,
    "leave_days": 2,
    "attendance_percentage": 92.31
  },
  "fees": {
    "total_fee": 60000,
    "paid_fee": 55000,
    "pending_fee": 5000,
    "fee_percentage": 91.67
  },
  "marks": {
    "total_exams": 20,
    "average_percentage": 85.5,
    "total_marks_obtained": 1710,
    "total_marks": 2000,
    "marks_by_subject": [
      {
        "subject": "Mathematics",
        "total_marks": 500,
        "marks_obtained": 425,
        "exams": 5,
        "average_percentage": 85.0
      }
    ]
  },
  "homework": {
    "assigned": 3,
    "submitted": 5,
    "evaluated": 2,
    "average_marks": 88.5
  },
  "recent_homework": [
    {
      "subject": "Math",
      "title": "Chapter 5 Exercises",
      "due_date": "10-01-2024",
      "status": "Assigned"
    }
  ],
  "recent_marks": [
    {
      "exam_name": "Unit Test 1",
      "subject": "Math",
      "marks_obtained": 85,
      "total_marks": 100,
      "percentage": 85.0,
      "grade": "A",
      "exam_date": "01-01-2024"
    }
  ]
}
```

---

### 3. Attendance Endpoints

#### Get Attendance Summary
```
GET /api/students/{student_id}/attendance

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1/attendance"

Response: 200 OK
{
  "summary": {
    "total_days": 130,
    "present_days": 120,
    "absent_days": 8,
    "leave_days": 2,
    "attendance_percentage": 92.31
  },
  "recent_records": [
    {
      "date": "10-01-2024",
      "status": "Present",
      "remarks": null
    },
    {
      "date": "09-01-2024",
      "status": "Absent",
      "remarks": "Sick"
    }
  ]
}
```

#### Get Attendance Details
```
GET /api/attendance/student/{student_id}

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/attendance/student/1"

Response: 200 OK
{
  "student": "Rahul",
  "summary": {
    "total_days": 130,
    "present_days": 120,
    "absent_days": 8,
    "leave_days": 2,
    "attendance_percentage": 92.31
  },
  "recent_records": [
    {
      "date": "10-01-2024",
      "status": "Present",
      "remarks": null
    }
  ]
}
```

---

### 4. Fee Endpoints

#### Get Fee Details
```
GET /api/students/{student_id}/fees

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1/fees"

Response: 200 OK
{
  "summary": {
    "total_fee": 60000,
    "paid_fee": 55000,
    "pending_fee": 5000,
    "fee_percentage": 91.67
  },
  "pending_fees": [
    {
      "month": "02-2024",
      "amount": 5000,
      "paid_amount": 0,
      "pending_amount": 5000,
      "status": "Pending",
      "due_date": "15-02-2024"
    }
  ]
}
```

#### Get Fees via Fees API
```
GET /api/fees/student/{student_id}

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/fees/student/1"

Response: 200 OK
{
  "student": "Rahul",
  "summary": {
    "total_fee": 60000,
    "paid_fee": 55000,
    "pending_fee": 5000,
    "fee_percentage": 91.67
  },
  "pending_fees": [...]
}
```

---

### 5. Marks Endpoints

#### Get Marks Summary
```
GET /api/students/{student_id}/marks

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1/marks"

Response: 200 OK
{
  "summary": {
    "total_exams": 20,
    "average_percentage": 85.5,
    "total_marks_obtained": 1710,
    "total_marks": 2000,
    "marks_by_subject": [
      {
        "subject": "Mathematics",
        "total_marks": 500,
        "marks_obtained": 425,
        "exams": 5,
        "average_percentage": 85.0
      }
    ]
  },
  "recent_marks": [
    {
      "exam_name": "Unit Test 1",
      "subject": "Math",
      "marks_obtained": 85,
      "total_marks": 100,
      "percentage": 85.0,
      "grade": "A",
      "exam_date": "01-01-2024"
    }
  ]
}
```

#### Get Marks via Marks API
```
GET /api/marks/student/{student_id}

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/marks/student/1"

Response: 200 OK
{
  "student": "Rahul",
  "summary": {...},
  "recent_marks": [...]
}
```

---

### 6. Homework Endpoints

#### Get Homework
```
GET /api/students/{student_id}/homework

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/students/1/homework"

Response: 200 OK
{
  "summary": {
    "assigned": 3,
    "submitted": 5,
    "evaluated": 2,
    "average_marks": 88.5
  },
  "pending_homework": [
    {
      "subject": "Math",
      "title": "Chapter 5 Exercises",
      "due_date": "10-01-2024",
      "status": "Assigned"
    }
  ]
}
```

#### Get Homework via Homework API
```
GET /api/homework/student/{student_id}

Parameters:
- student_id: integer

Example:
curl "http://localhost:8000/api/homework/student/1"

Response: 200 OK
{
  "student": "Rahul",
  "summary": {...},
  "pending_homework": [...]
}
```

---

### 7. WhatsApp Webhook Endpoint

#### Receive WhatsApp Message
```
POST /api/whatsapp/webhook
Content-Type: application/x-www-form-urlencoded

Parameters (from Twilio):
- From: string - WhatsApp phone (e.g., whatsapp:+6302894103)
- Body: string - Message text
- MessageSid: string - Twilio message ID

Example:
curl -X POST "http://localhost:8000/api/whatsapp/webhook" \
  -d "From=whatsapp%3A%2B6302894103&Body=Hi&MessageSid=SMxxxxx"

Response: 200 OK
{
  "status": "success",
  "message_sid": "SMxxxxx",
  "menu_state": "main"
}
```

#### Send WhatsApp Message (Admin)
```
POST /api/whatsapp/send

Parameters:
- to_phone: string - Recipient phone
- message: string - Message content

Example:
curl -X POST "http://localhost:8000/api/whatsapp/send" \
  -d "to_phone=%2B6302894103&message=Hello%20from%20AIRA"

Response: 200 OK
{
  "status": "success",
  "recipient": "whatsapp:+6302894103",
  "message": "Hello from AIRA"
}
```

#### WhatsApp Health Check
```
GET /api/whatsapp/health

Example:
curl "http://localhost:8000/api/whatsapp/health"

Response: 200 OK
{
  "status": "healthy",
  "twilio_configured": true,
  "whatsapp_number": "whatsapp:+14155552671"
}
```

---

### 8. System Endpoints

#### Health Check
```
GET /health

Example:
curl "http://localhost:8000/health"

Response: 200 OK
{
  "status": "healthy",
  "service": "AIRA - WhatsApp Parent Assistant",
  "version": "1.0.0"
}
```

#### Root Endpoint
```
GET /

Example:
curl "http://localhost:8000/"

Response: 200 OK
{
  "name": "AIRA - WhatsApp Parent Assistant",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "redoc": "/redoc",
  "endpoints": {...}
}
```

---

## WhatsApp Conversation Flow Examples

### Scenario 1: Single Student Parent

**Parent:** "Hi"
**Bot:**
```
Hello Rajesh Sharma! 👋

Welcome to AIRA Parent Assistant.

Please select an option:

1️⃣  Student Profile
2️⃣  Attendance
3️⃣  Fee Details
4️⃣  Marks
5️⃣  Homework

Reply with the number of your choice.
```

**Parent:** "1"
**Bot:**
```
📚 RAHUL - Student Profile

Class: 8A
Roll Number: 001
Email: rahul@school.com

📊 ATTENDANCE: 92.31%
Present: 120/130 days

💰 FEE STATUS: ₹5,000 Pending
Paid: ₹55,000 / ₹60,000

📈 MARKS: 85.5% Average
Total Exams: 20

📝 HOMEWORK:
Assigned: 3, Submitted: 5, Evaluated: 2

0️⃣  Back to Main Menu

Reply with 0 to go back.
```

---

### Scenario 2: Multiple Students Parent

**Parent:** "Hi"
**Bot:** (Main menu with options)

**Parent:** "1"
**Bot:**
```
Please select a student:

1️⃣  Rahul (Class 8A)
2️⃣  Priya (Class 5B)

Reply with the number.
```

**Parent:** "1"
**Bot:** (Student profile for Rahul)

**Parent:** "0"
**Bot:** (Back to main menu)

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Student not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["query", "student_id"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "detail": "Internal server error"
}
```

---

## Rate Limiting (Future)

Currently not implemented. For production, add:

```bash
pip install slowapi
```

Usage limits:
- `/api/students` - 100 req/hour
- `/api/whatsapp/webhook` - 1000 req/hour
- `/api/parents` - 50 req/hour

---

## Pagination (Future)

```
GET /api/students?page=1&limit=10&offset=0

Response includes:
- total: int
- page: int
- limit: int
- items: []
```

---

## Filtering (Future)

```
GET /api/students?class=8&status=active

Response: Filtered results
```

---

## Tools for Testing

### cURL
```bash
curl -X GET "http://localhost:8000/health"
```

### Postman
1. Import API from `/docs`
2. Create collections
3. Test endpoints

### httpie
```bash
pip install httpie
http GET localhost:8000/health
```

### Python Requests
```python
import requests

response = requests.get("http://localhost:8000/api/parents/+6302894103")
print(response.json())
```

### JavaScript/Node.js
```javascript
fetch("http://localhost:8000/health")
  .then(r => r.json())
  .then(data => console.log(data))
```

---

## WebHook Signature Validation (Production)

For production with Twilio:

```python
from twilio.request_validator import RequestValidator

validator = RequestValidator(auth_token)
request_url = f"https://mycompany.com/api/whatsapp/webhook"

# Validate before processing
is_valid = validator.validate(
    request_url,
    request.form,
    request.headers.get('X-Twilio-Signature', '')
)

if not is_valid:
    return {"status": "unauthorized"}, 403
```

---

## Monitoring & Analytics

### Endpoint Usage
```bash
GET /api/analytics/endpoints
Response: { endpoint: usage_count }
```

### Error Tracking
```bash
GET /api/analytics/errors
Response: { error_type: count }
```

### WhatsApp Stats
```bash
GET /api/analytics/whatsapp
Response: { messages_sent, messages_received, avg_response_time }
```

---

For complete API documentation with live examples, visit:
**http://localhost:8000/docs**
