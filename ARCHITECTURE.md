# AIRA Architecture Documentation

## System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Parent (WhatsApp User)                        │
│                        WhatsApp Enabled Phone                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ WhatsApp Message
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Twilio WhatsApp Sandbox                           │
│                   (Production: Meta API)                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTP POST (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FastAPI Web Server                               │
│                      (Uvicorn ASGI)                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  API Routes Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │   │
│  │  │ WhatsApp API │  │ Parent API   │  │ Admin API        │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │   │
│  └──────────────────────┬────────────────────────────────────────┘  │
│                         │                                            │
│  ┌──────────────────────▼────────────────────────────────────────┐  │
│  │               Services Layer (Business Logic)                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │WhatsApp Svc  │  │Parent Svc    │  │Student Svc       │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │Fee Svc       │  │Attendance Svc│  │Marks Svc         │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │  │
│  └──────────────────────┬────────────────────────────────────────┘  │
│                         │                                            │
│  ┌──────────────────────▼────────────────────────────────────────┐  │
│  │          Database Access Layer (Schemas & Models)            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │Pydantic      │  │SQLAlchemy    │  │ORM Relationships │    │  │
│  │  │Schemas       │  │Models        │  │                  │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │  │
│  └──────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────────────┘
                          │
                          │ SQL Queries
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SQLite Database                                 │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐            │
│  │ Parents      │  │ Students     │  │ Attendance       │            │
│  └──────────────┘  └──────────────┘  └──────────────────┘            │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐            │
│  │ Fees         │  │ Homework     │  │ Marks            │            │
│  └──────────────┘  └──────────────┘  └──────────────────┘            │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐                                   │
│  │ Classes      │  │ Sessions     │                                   │
│  └──────────────┘  └──────────────┘                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Description

### 1. API Layer (`app/api/routes/`)

**WhatsApp Route** (`whatsapp.py`)
- Receives incoming WhatsApp messages via Twilio webhook
- Validates message authenticity
- Routes to appropriate handler
- Sends response back via Twilio

**Parent Route** (`parent.py`)
- Get parent by phone number
- Get parent's students list
- Create parent (admin only)

**Student Route** (`student.py`)
- Get student profile
- Get comprehensive student data with stats
- List all students (admin)

**Attendance Route** (`attendance.py`)
- Get attendance summary
- Get detailed attendance records
- Calculate attendance percentage

**Fee Route** (`fees.py`)
- Get fee details
- Get outstanding fees
- Payment history

**Homework Route** (`homework.py`)
- Get pending homework
- Get homework history
- Homework status tracking

**Marks Route** (`marks.py`)
- Get exam marks
- Get marks by subject
- Calculate grade

### 2. Services Layer (`app/services/`)

Implements business logic and data processing:

**WhatsApp Service** (`whatsapp_service.py`)
- Parse incoming messages
- Manage conversation state (session)
- Generate appropriate responses
- Format messages for WhatsApp

**Parent Service** (`parent_service.py`)
- Authenticate parent by phone
- Get parent data
- Get parent's students

**Student Service** (`student_service.py`)
- Calculate attendance percentage
- Calculate average marks
- Get comprehensive student profile

**Fee Service** (`fees_service.py`)
- Calculate outstanding fees
- Get fee status
- Payment calculations

### 3. Integration Layer (`app/integrations/`)

**Twilio Client** (`twilio_client.py`)
- Send WhatsApp messages
- Validate incoming messages
- Handle Twilio credentials

### 4. Database Layer

**Engine** (`app/database/engine.py`)
- SQLAlchemy engine initialization
- Session management
- Database connection pooling

**Models** (`app/models/models.py`)
- SQLAlchemy ORM models
- Database relationships
- Table definitions

**Schemas** (`app/schemas/schemas.py`)
- Pydantic request/response models
- Data validation
- Type hints

## Data Flow

### WhatsApp Message Flow

1. **Parent sends WhatsApp message**
   ```
   Parent: "Hi"
   ```

2. **Twilio receives and forwards to webhook**
   ```
   POST /api/whatsapp/webhook
   {
     "From": "whatsapp:+6302894103",
     "Body": "Hi",
     "MessageSid": "..."
   }
   ```

3. **FastAPI receives request**
   - Validates Twilio signature
   - Parses message body
   - Extracts sender phone number

4. **WhatsApp Service processes**
   - Gets parent from database by phone
   - Checks or creates session
   - Determines current menu state
   - Generates appropriate response

5. **Response generated**
   ```
   "Welcome to AIRA! Please select:
    1. Student Profile
    2. Attendance
    ..."
   ```

6. **Twilio sends response**
   ```
   POST https://api.twilio.com/send
   {
     "To": "whatsapp:+6302894103",
     "Body": "Welcome message..."
   }
   ```

7. **Parent receives on WhatsApp**

## Session Management

### Session Storage

Sessions are stored in `ParentSession` table:

```python
{
  id: 1,
  parent_id: 1,
  current_student_id: None,  # Selected student
  current_menu: "main",       # Current menu: main, student_select, etc.
  session_data: "{}",         # Additional JSON data
  created_at: datetime,
  updated_at: datetime
}
```

### Menu States

```
Main Menu
├── 1 → Student Profile
│   └── Student Selection → Detailed Profile
├── 2 → Attendance
│   └── Student Selection → Attendance Details
├── 3 → Fee Details
│   └── Student Selection → Fee Details
├── 4 → Marks
│   └── Student Selection → Marks Details
└── 5 → Homework
    └── Student Selection → Homework Details
```

## Authentication & Authorization (MVP)

**Current (MVP):**
- Phone number from WhatsApp is treated as parent identity
- Data scoped to parent's students only
- No OTP required

**Future (Phase 2+):**
- OTP verification
- Role-based access control (Parent, Admin, Teacher)
- Encrypted session tokens

## Error Handling Strategy

```python
# Validation Errors
- Invalid phone number format
- Student not found
- Parent not found

# Processing Errors
- Database connection failures
- Calculation errors
- Twilio API failures

# Response Errors
- Formatted error messages for user
- Logging for debugging
- Graceful degradation
```

## Performance Considerations

### Database Optimization
- Indexes on frequently queried fields (phone_number, student_id)
- Relationship lazy loading where appropriate
- Query optimization in services layer

### Caching Strategy
- Parent data cached during session
- Session timeout: 1 hour
- Student list cache

### Scalability
- SQLite for MVP (suitable for <10K records)
- Easy migration to PostgreSQL
- Connection pooling configured
- Async-ready architecture

## Deployment Architecture

### Local Development
```
Uvicorn (Debug Mode)
└── SQLite Database
```

### Production (Future)
```
Nginx (Reverse Proxy)
    ↓
Gunicorn (Production ASGI Server)
    ├── FastAPI Instance 1
    ├── FastAPI Instance 2
    └── FastAPI Instance N
        ↓
    PostgreSQL Database
        ↓
    Redis Cache
```

## Configuration Management

**Settings Hierarchy:**
1. Environment variables (.env file)
2. Default values in config.py
3. Runtime overrides via Pydantic Settings

**Key Settings:**
- Database URL
- Twilio credentials
- API settings
- Logging configuration
- Session timeout

## Logging & Monitoring

**Log Levels:**
- DEBUG: Detailed development information
- INFO: General application events
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

**Log Destinations:**
- Console (development)
- File (logs/aira.log)
- Structured logging (future: ELK stack)

## Testing Strategy

### Unit Tests
- Service layer logic
- Schema validation
- Utility functions

### Integration Tests
- API endpoints
- Database operations
- Twilio integration

### Test Coverage
- Target: >80% code coverage
- Critical paths: 100%
- Mock external APIs

## Security Best Practices

### Input Validation
- All user inputs validated via Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention

### Data Protection
- Sensitive data not logged
- HTTPS/SSL enforced (production)
- Session timeout
- Rate limiting (future)

### Compliance
- Data privacy (GDPR ready)
- School data protection
- Parent consent management (future)

## Extensibility

### Adding New Features
1. Define schema in `schemas.py`
2. Create model in `models.py`
3. Add service in `services/`
4. Create route in `api/routes/`
5. Add tests

### Adding New Integrations
1. Create integration file in `app/integrations/`
2. Implement client class
3. Add to services
4. Use in routes

## Documentation

- **API Docs**: Swagger UI at `/docs`
- **Architecture**: This file
- **Setup**: README.md
- **Code Comments**: Inline documentation
- **Database**: Entity-Relationship Diagram (ERD)

---

This architecture is designed to be:
- **Scalable**: Easy to add new features
- **Maintainable**: Clear separation of concerns
- **Testable**: Easy to unit test
- **Performant**: Optimized queries
- **Secure**: Input validation and authorization
