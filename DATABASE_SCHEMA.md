# AIRA Database Schema

## Entity-Relationship Diagram (Conceptual)

```
┌──────────────────┐
│     Class        │
├──────────────────┤
│ id (PK)          │
│ name             │
│ created_at       │
└──────┬───────────┘
       │ 1:N
       │
       ▼
┌──────────────────┐         ┌──────────────────┐
│    Student       │◄────────┤     Parent       │
├──────────────────┤  N:1    ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ name             │         │ phone_number (U) │
│ roll_number (U)  │         │ name             │
│ parent_id (FK)   │         │ email            │
│ class_id (FK)    │         │ alternate_phone  │
│ email            │         │ created_at       │
│ created_at       │         │ is_active        │
│ is_active        │         └──────┬───────────┘
└──────┬───────────┘                │ 1:N
       │                            │
       │ 1:N                        ▼
       │                    ┌──────────────────────┐
       │                    │  ParentSession       │
       │                    ├──────────────────────┤
       ├────────────────┬──►│ id (PK)              │
       │                │   │ parent_id (FK)       │
       │                │   │ current_student_id   │
       │                │   │ current_menu         │
       │                │   │ session_data         │
       │                │   │ created_at           │
       │                │   │ updated_at           │
       │                │   └──────────────────────┘
       │                │
       │ 1:N            │
       ├────┬───────────┘
       │    │
       ▼    ▼
    ┌──────────────────┬──────────────────┬──────────────────┐
    │  Attendance      │      Fee         │    Homework      │
    ├──────────────────┼──────────────────┼──────────────────┤
    │ id (PK)          │ id (PK)          │ id (PK)          │
    │ student_id (FK)  │ student_id (FK)  │ student_id (FK)  │
    │ date             │ month            │ subject          │
    │ status           │ amount           │ title            │
    │ remarks          │ paid_amount      │ description      │
    │ created_at       │ status           │ due_date         │
    └──────────────────┤ due_date         │ assigned_date    │
                       │ payment_date     │ status           │
                       │ remarks          │ marks_obtained   │
                       │ created_at       │ total_marks      │
                       └──────────────────┤ created_at       │
                                          └──────────────────┘

    ┌──────────────────┐
    │     Mark         │
    ├──────────────────┤
    │ id (PK)          │
    │ student_id (FK)  │
    │ exam_name        │
    │ subject          │
    │ marks_obtained   │
    │ total_marks      │
    │ percentage       │
    │ grade            │
    │ exam_date        │
    │ created_at       │
    └──────────────────┘
```

## Table Definitions

### 1. Parent Table

**Purpose:** Store parent/guardian information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| phone_number | VARCHAR(20) | UNIQUE, INDEX | WhatsApp phone number (format: +6302894103) |
| name | VARCHAR(100) | INDEX | Parent/Guardian name |
| email | VARCHAR(100) | NULLABLE | Email address |
| alternate_phone | VARCHAR(20) | NULLABLE | Alternate contact number |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |

**Indexes:**
- `idx_parent_phone_number` - For quick parent lookup by phone

**Relationships:**
- 1:N → Student (one parent can have multiple students)
- 1:N → ParentSession (one parent can have multiple sessions)

---

### 2. Class Table

**Purpose:** Store school class information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(50) | UNIQUE, INDEX | Class name (e.g., "5A", "8B", "10 Commerce") |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Relationships:**
- 1:N → Student (one class has multiple students)

---

### 3. Student Table

**Purpose:** Store student information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| name | VARCHAR(100) | INDEX | Student name |
| roll_number | VARCHAR(50) | UNIQUE, INDEX | Unique roll number |
| parent_id | INTEGER | FK(Parent.id), INDEX | Parent reference |
| class_id | INTEGER | FK(Class.id), INDEX | Class reference |
| email | VARCHAR(100) | NULLABLE | Student email |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |

**Indexes:**
- `idx_student_parent_id` - For getting all students of a parent
- `idx_student_class_id` - For getting all students in a class
- `idx_student_roll_number` - For unique identification

**Relationships:**
- N:1 → Parent (many students per parent, one parent per student)
- N:1 → Class (many students per class, one class per student)
- 1:N → Attendance
- 1:N → Fee
- 1:N → Homework
- 1:N → Mark

---

### 4. Attendance Table

**Purpose:** Store daily attendance records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| student_id | INTEGER | FK(Student.id), INDEX | Student reference |
| date | DATE | INDEX | Attendance date |
| status | VARCHAR(20) | | Status: "Present", "Absent", "Leave" |
| remarks | TEXT | NULLABLE | Reason or additional notes |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Indexes:**
- `idx_attendance_student_date` - For getting attendance records by student and date range

**Sample Data:**
```
| id | student_id | date | status | remarks |
|----|------------|------|--------|---------|
| 1 | 1 | 2024-01-02 | Present | - |
| 2 | 1 | 2024-01-03 | Absent | Sick |
| 3 | 1 | 2024-01-04 | Leave | Family event |
```

---

### 5. Fee Table

**Purpose:** Store monthly fee records and payment status

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| student_id | INTEGER | FK(Student.id), INDEX | Student reference |
| month | VARCHAR(20) | | Month identifier (e.g., "January-2024", "01-2024") |
| amount | FLOAT | | Total fee amount |
| paid_amount | FLOAT | DEFAULT 0 | Amount paid so far |
| status | VARCHAR(20) | | Status: "Paid", "Pending", "Partial" |
| due_date | DATE | | Payment deadline |
| payment_date | DATE | NULLABLE | Actual payment date |
| remarks | TEXT | NULLABLE | Payment notes or reasons for delay |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Indexes:**
- `idx_fee_student_month` - For getting fee records by student and month

**Sample Data:**
```
| id | student_id | month | amount | paid_amount | status | due_date |
|----|------------|-------|--------|-------------|--------|----------|
| 1 | 1 | January-2024 | 5000 | 5000 | Paid | 2024-01-15 |
| 2 | 1 | February-2024 | 5000 | 0 | Pending | 2024-02-15 |
| 3 | 1 | March-2024 | 5000 | 2500 | Partial | 2024-03-15 |
```

---

### 6. Homework Table

**Purpose:** Store homework assignments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| student_id | INTEGER | FK(Student.id), INDEX | Student reference |
| subject | VARCHAR(100) | | Subject name (e.g., "Mathematics", "English") |
| title | VARCHAR(255) | | Homework title |
| description | TEXT | | Detailed description of assignment |
| due_date | DATE | | Submission deadline |
| assigned_date | DATE | | Date homework was assigned |
| status | VARCHAR(20) | | Status: "Assigned", "Submitted", "Evaluated" |
| marks_obtained | FLOAT | NULLABLE | Marks scored (if evaluated) |
| total_marks | FLOAT | DEFAULT 100 | Total marks for this homework |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Indexes:**
- `idx_homework_student_date` - For getting homework by student and date

**Sample Data:**
```
| id | student_id | subject | title | due_date | status |
|----|------------|---------|-------|----------|--------|
| 1 | 1 | Math | Chapter 5 Exercises | 2024-01-10 | Submitted |
| 2 | 1 | English | Essay on Environment | 2024-01-15 | Assigned |
| 3 | 1 | Science | Project on Solar System | 2024-01-20 | Assigned |
```

---

### 7. Mark Table

**Purpose:** Store exam results and marks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| student_id | INTEGER | FK(Student.id), INDEX | Student reference |
| exam_name | VARCHAR(100) | | Exam type (e.g., "Unit Test 1", "Mid Term", "Final") |
| subject | VARCHAR(100) | | Subject name |
| marks_obtained | FLOAT | | Marks scored |
| total_marks | FLOAT | DEFAULT 100 | Total marks for exam |
| percentage | FLOAT | | Percentage: (marks_obtained/total_marks)*100 |
| grade | VARCHAR(5) | NULLABLE | Grade letter (A, B, C, D, F) |
| exam_date | DATE | | Date of examination |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Indexes:**
- `idx_mark_student_exam` - For getting marks by student and exam

**Sample Data:**
```
| id | student_id | exam_name | subject | marks_obtained | percentage | grade | exam_date |
|----|------------|-----------|---------|-----------------|------------|-------|-----------|
| 1 | 1 | Unit Test 1 | Math | 45 | 90 | A | 2024-01-20 |
| 2 | 1 | Unit Test 1 | English | 42 | 84 | B | 2024-01-22 |
| 3 | 1 | Unit Test 1 | Science | 43 | 86 | A | 2024-01-25 |
```

---

### 8. ParentSession Table

**Purpose:** Manage WhatsApp conversation state for each parent

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier |
| parent_id | INTEGER | FK(Parent.id), INDEX | Parent reference |
| current_student_id | INTEGER | FK(Student.id), NULLABLE | Currently selected student (if any) |
| current_menu | VARCHAR(50) | DEFAULT "main" | Current menu state |
| session_data | TEXT | NULLABLE | Additional session data (JSON format) |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Session start time |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last activity time |

**Indexes:**
- `idx_session_parent_id` - For quick session lookup by parent

**Current Menu States:**
```
main                    - Main menu
student_select          - Student selection
student_profile         - Showing student profile
attendance_menu         - Attendance submenu
attendance_details      - Detailed attendance
fees_menu               - Fees submenu
fees_details            - Detailed fees
marks_menu              - Marks submenu
marks_details           - Detailed marks
homework_menu           - Homework submenu
homework_details        - Detailed homework
```

**Sample Session Data (JSON):**
```json
{
  "last_action": "selected_student",
  "timestamp": "2024-01-10T14:30:00Z",
  "previous_menu": "main"
}
```

---

## Database Constraints & Relationships

### Primary Keys
- All tables have `id` as PRIMARY KEY with auto-increment

### Foreign Keys
- Student.parent_id → Parent.id
- Student.class_id → Class.id
- Attendance.student_id → Student.id
- Fee.student_id → Student.id
- Homework.student_id → Student.id
- Mark.student_id → Student.id
- ParentSession.parent_id → Parent.id
- ParentSession.current_student_id → Student.id

### Unique Constraints
- Parent.phone_number - Unique parent per phone
- Student.roll_number - Unique roll number
- Class.name - Unique class name

### Cascade Rules
- Parent deletion → Cascade to Student, ParentSession
- Student deletion → Cascade to Attendance, Fee, Homework, Mark

---

## Indexes for Performance

### Critical Indexes
```sql
-- Quick parent lookup
CREATE INDEX idx_parent_phone_number ON parents(phone_number);

-- Get parent's students
CREATE INDEX idx_student_parent_id ON students(parent_id);

-- Get class students
CREATE INDEX idx_student_class_id ON students(class_id);

-- Session lookup
CREATE INDEX idx_session_parent_id ON parent_sessions(parent_id);

-- Attendance queries
CREATE INDEX idx_attendance_student_date ON attendance(student_id, date DESC);

-- Fee queries
CREATE INDEX idx_fee_student_month ON fees(student_id, month);

-- Homework queries
CREATE INDEX idx_homework_student_date ON homework(student_id, due_date DESC);

-- Mark queries
CREATE INDEX idx_mark_student_exam ON marks(student_id, exam_name);
```

---

## Database Statistics

### Typical MVP Data Volumes

```
Parents:              10 records
Classes:              8 records (Class 5-12)
Students:             20 records (2-3 per parent)
Attendance:           ~2,500 records (130 days × 20 students)
Fees:                 ~240 records (12 months × 20 students)
Homework:             ~200 records (10 per student)
Marks:                ~400 records (4 exams × 5 subjects × 20 students)
ParentSession:        10 records (1 per parent, active sessions)

Total Records:        ~3,380
Database Size:        < 5 MB
```

---

## Migration Path

### SQLite to PostgreSQL (Future)

```sql
-- Most of the schema transfers directly
-- Only changes needed:
-- 1. DATETIME → TIMESTAMP
-- 2. VARCHAR(n) → VARCHAR or TEXT
-- 3. BOOLEAN remains same
-- 4. No other schema changes required
```

---

## Backup & Recovery Strategy

### Backup
```bash
# SQLite backup
sqlite3 aira.db ".backup aira_backup.db"
```

### Recovery
```bash
# Restore from backup
sqlite3 aira.db ".restore aira_backup.db"
```

---

This database schema is designed to be:
- **Normalized**: Reduces data redundancy
- **Scalable**: Indexes for performance
- **Maintainable**: Clear relationships
- **Flexible**: Easy to add new features
- **Compliant**: Supports school data management
