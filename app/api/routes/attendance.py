"""
Attendance API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.services.student_service import StudentService
from app.models.models import Student

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.get("/student/{student_id}")
async def get_attendance(student_id: int, db: Session = Depends(get_db)):
    """Get attendance for a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_attendance_summary(db, student_id)
    details = StudentService.get_attendance_details(db, student_id, limit=60)
    
    return {
        "student": student.name,
        "summary": summary.dict(),
        "recent_records": details
    }
