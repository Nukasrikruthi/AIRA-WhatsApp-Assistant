"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


# ============= Class Schemas =============
class ClassBase(BaseModel):
    name: str


class ClassCreate(ClassBase):
    pass


class ClassResponse(ClassBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Parent Schemas =============
class ParentBase(BaseModel):
    phone_number: str
    name: str
    email: Optional[str] = None
    alternate_phone: Optional[str] = None


class ParentCreate(ParentBase):
    pass


class ParentResponse(ParentBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ParentDetailResponse(ParentResponse):
    students: List['StudentResponse'] = []


# ============= Student Schemas =============
class StudentBase(BaseModel):
    name: str
    roll_number: str
    email: Optional[str] = None


class StudentCreate(StudentBase):
    parent_id: int
    class_id: int


class StudentResponse(StudentBase):
    id: int
    parent_id: int
    class_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentDetailResponse(StudentResponse):
    class_obj: Optional[ClassResponse] = None


# ============= Attendance Schemas =============
class AttendanceBase(BaseModel):
    date: date
    status: str  # Present, Absent, Leave
    remarks: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    student_id: int


class AttendanceResponse(AttendanceBase):
    id: int
    student_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentAttendanceSummary(BaseModel):
    total_days: int = 0
    present_days: int = 0
    absent_days: int = 0
    leave_days: int = 0
    attendance_percentage: float = 0.0


# ============= Fee Schemas =============
class FeeBase(BaseModel):
    month: str
    amount: float
    status: str  # Paid, Pending, Partial
    due_date: date
    payment_date: Optional[date] = None
    remarks: Optional[str] = None


class FeeCreate(FeeBase):
    student_id: int
    paid_amount: float = 0


class FeeResponse(FeeBase):
    id: int
    student_id: int
    paid_amount: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentFeesSummary(BaseModel):
    total_fee: float = 0.0
    paid_fee: float = 0.0
    pending_fee: float = 0.0
    fee_percentage: float = 0.0


# ============= Homework Schemas =============
class HomeworkBase(BaseModel):
    subject: str
    title: str
    description: str
    due_date: date
    assigned_date: date
    status: str = "Assigned"  # Assigned, Submitted, Evaluated


class HomeworkCreate(HomeworkBase):
    student_id: int
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = 100


class HomeworkResponse(HomeworkBase):
    id: int
    student_id: int
    marks_obtained: Optional[float]
    total_marks: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Mark Schemas =============
class MarkBase(BaseModel):
    exam_name: str
    subject: str
    marks_obtained: float
    total_marks: float = 100
    percentage: float
    grade: Optional[str] = None
    exam_date: date


class MarkCreate(MarkBase):
    student_id: int


class MarkResponse(MarkBase):
    id: int
    student_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudentMarksSummary(BaseModel):
    total_exams: int = 0
    average_percentage: float = 0.0
    total_marks_obtained: float = 0.0
    total_marks: float = 0.0
    marks_by_subject: List[dict] = []


# ============= Session Schemas =============
class ParentSessionBase(BaseModel):
    current_menu: str = "main"


class ParentSessionResponse(ParentSessionBase):
    id: int
    parent_id: int
    current_student_id: Optional[int] = None
    session_data: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============= WhatsApp Schemas =============
class WhatsAppMessageRequest(BaseModel):
    """Twilio WhatsApp incoming message"""
    MessageSid: str
    AccountSid: str
    From: str
    To: str
    Body: str
    MediaContentType0: Optional[str] = None


class WhatsAppMessageResponse(BaseModel):
    """WhatsApp message response"""
    message: str
    user_choice: Optional[str] = None


# ============= Comprehensive Student Profile =============
class StudentProfileResponse(BaseModel):
    student: StudentDetailResponse
    attendance: StudentAttendanceSummary
    fees: StudentFeesSummary
    marks: StudentMarksSummary
    recent_homework: List[HomeworkResponse]
    
    class Config:
        from_attributes = True


# Update forward references
ParentDetailResponse.model_rebuild()
StudentDetailResponse.model_rebuild()
