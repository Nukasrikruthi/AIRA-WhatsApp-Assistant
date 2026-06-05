"""
Homework API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.services.student_service import StudentService
from app.models.models import Student

router = APIRouter(prefix="/api/homework", tags=["Homework"])


@router.get("/student/{student_id}")
async def get_homework(student_id: int, db: Session = Depends(get_db)):
    """Get homework for a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_homework_summary(db, student_id)
    pending = StudentService.get_pending_homework(db, student_id)
    
    return {
        "student": student.name,
        "summary": summary,
        "pending_homework": pending
    }
