"""
SQLAlchemy models for AIRA database
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.engine import Base


class Class(Base):
    """Class model"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    students = relationship("Student", back_populates="class_obj")
    
    class Config:
        arbitrary_types_allowed = True


class Parent(Base):
    """Parent model"""
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    students = relationship("Student", back_populates="parent")
    sessions = relationship("ParentSession", back_populates="parent", cascade="all, delete-orphan")
    
    class Config:
        arbitrary_types_allowed = True


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    roll_number = Column(String(50), unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), index=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    parent = relationship("Parent", back_populates="students")
    class_obj = relationship("Class", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    fee_records = relationship("Fee", back_populates="student", cascade="all, delete-orphan")
    homework_records = relationship("Homework", back_populates="student", cascade="all, delete-orphan")
    mark_records = relationship("Mark", back_populates="student", cascade="all, delete-orphan")
    
    class Config:
        arbitrary_types_allowed = True


class Attendance(Base):
    """Attendance model"""
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    date = Column(Date, index=True)
    status = Column(String(20))  # Present, Absent, Leave
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    
    class Config:
        arbitrary_types_allowed = True


class Fee(Base):
    """Fee model"""
    __tablename__ = "fees"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    month = Column(String(20))  # Month name or month-year
    amount = Column(Float)
    paid_amount = Column(Float, default=0)
    status = Column(String(20))  # Paid, Pending, Partial
    due_date = Column(Date)
    payment_date = Column(Date, nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="fee_records")
    
    class Config:
        arbitrary_types_allowed = True


class Homework(Base):
    """Homework model"""
    __tablename__ = "homework"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    subject = Column(String(100))
    title = Column(String(255))
    description = Column(Text)
    due_date = Column(Date)
    assigned_date = Column(Date)
    status = Column(String(20))  # Assigned, Submitted, Evaluated
    marks_obtained = Column(Float, nullable=True)
    total_marks = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="homework_records")
    
    class Config:
        arbitrary_types_allowed = True


class Mark(Base):
    """Marks/Exam Results model"""
    __tablename__ = "marks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    exam_name = Column(String(100))  # Unit Test 1, Mid Term, Final, etc.
    subject = Column(String(100))
    marks_obtained = Column(Float)
    total_marks = Column(Float, default=100)
    percentage = Column(Float)
    grade = Column(String(5), nullable=True)  # A, B, C, etc.
    exam_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="mark_records")
    
    class Config:
        arbitrary_types_allowed = True


class ParentSession(Base):
    """Parent session management for WhatsApp conversations"""
    __tablename__ = "parent_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), index=True)
    current_student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    current_menu = Column(String(50), default="main")  # main, student_select, etc.
    session_data = Column(Text, nullable=True)  # JSON format for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent = relationship("Parent", back_populates="sessions")
    
    class Config:
        arbitrary_types_allowed = True
