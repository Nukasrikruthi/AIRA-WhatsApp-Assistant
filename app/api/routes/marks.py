"""
Marks API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.services.student_service import StudentService
from app.models.models import Student

router = APIRouter(prefix="/api/marks", tags=["Marks"])


@router.get("/student/{student_id}")
async def get_marks(student_id: int, db: Session = Depends(get_db)):
    """Get marks for a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_marks_summary(db, student_id)
    recent = StudentService.get_recent_marks(db, student_id, limit=20)
    
    return {
        "student": student.name,
        "summary": summary.dict(),
        "recent_marks": recent
    }
