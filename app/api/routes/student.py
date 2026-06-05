"""
Student API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.schemas.schemas import (
    StudentResponse, StudentDetailResponse, StudentProfileResponse,
    StudentAttendanceSummary, StudentFeesSummary, StudentMarksSummary
)
from app.services.student_service import StudentService
from app.models.models import Student
from typing import List

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/{student_id}", response_model=StudentDetailResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get student details
    
    Args:
        student_id: Student ID
        
    Returns:
        Student information
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@router.get("/{student_id}/profile", response_model=dict)
async def get_student_profile(student_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive student profile
    
    Args:
        student_id: Student ID
        
    Returns:
        Complete profile with attendance, fees, marks, homework
    """
    profile = StudentService.get_comprehensive_profile(db, student_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return profile


@router.get("/{student_id}/attendance")
async def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    """
    Get attendance summary for student
    
    Args:
        student_id: Student ID
        
    Returns:
        Attendance statistics
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    attendance = StudentService.get_attendance_summary(db, student_id)
    details = StudentService.get_attendance_details(db, student_id)
    
    return {
        "summary": attendance.dict(),
        "recent_records": details
    }


@router.get("/{student_id}/attendance/details")
async def get_attendance_details(student_id: int, db: Session = Depends(get_db)):
    """
    Get detailed attendance records
    
    Args:
        student_id: Student ID
        
    Returns:
        Attendance records
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    details = StudentService.get_attendance_details(db, student_id, limit=100)
    
    return {"records": details}


@router.get("/{student_id}/fees")
async def get_student_fees(student_id: int, db: Session = Depends(get_db)):
    """
    Get fee summary for student
    
    Args:
        student_id: Student ID
        
    Returns:
        Fee statistics
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_fee_summary(db, student_id)
    pending = StudentService.get_pending_fees(db, student_id)
    
    return {
        "summary": summary.dict(),
        "pending_fees": pending
    }


@router.get("/{student_id}/marks")
async def get_student_marks(student_id: int, db: Session = Depends(get_db)):
    """
    Get marks summary for student
    
    Args:
        student_id: Student ID
        
    Returns:
        Marks statistics
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_marks_summary(db, student_id)
    recent = StudentService.get_recent_marks(db, student_id, limit=20)
    
    return {
        "summary": summary.dict(),
        "recent_marks": recent
    }


@router.get("/{student_id}/homework")
async def get_student_homework(student_id: int, db: Session = Depends(get_db)):
    """
    Get homework for student
    
    Args:
        student_id: Student ID
        
    Returns:
        Homework statistics
    """
    student = StudentService.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_homework_summary(db, student_id)
    pending = StudentService.get_pending_homework(db, student_id)
    
    return {
        "summary": summary,
        "pending_homework": pending
    }


@router.get("")
async def list_students(db: Session = Depends(get_db)):
    """
    List all students (Admin endpoint)
    
    Returns:
        List of all students
    """
    students = db.query(Student).filter(Student.is_active == True).all()
    
    return students
