"""
Fees API routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.services.student_service import StudentService
from app.models.models import Student

router = APIRouter(prefix="/api/fees", tags=["Fees"])


@router.get("/student/{student_id}")
async def get_fees(student_id: int, db: Session = Depends(get_db)):
    """Get fee details for a student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    summary = StudentService.get_fee_summary(db, student_id)
    pending = StudentService.get_pending_fees(db, student_id)
    
    return {
        "student": student.name,
        "summary": summary.dict(),
        "pending_fees": pending
    }
