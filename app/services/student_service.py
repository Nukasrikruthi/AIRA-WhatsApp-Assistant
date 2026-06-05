"""
Student service - Handle student-related business logic
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import (
    Student, Attendance, Fee, Mark, Homework
)
from app.schemas.schemas import (
    StudentAttendanceSummary, StudentFeesSummary, StudentMarksSummary, StudentProfileResponse
)
from typing import Optional, List
from datetime import date


class StudentService:
    """Service for student operations"""
    
    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        return db.query(Student).filter(
            Student.id == student_id,
            Student.is_active == True
        ).first()
    
    @staticmethod
    def get_attendance_summary(db: Session, student_id: int) -> StudentAttendanceSummary:
        """
        Calculate attendance summary for a student
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            StudentAttendanceSummary with attendance statistics
        """
        # Get all attendance records
        attendance_records = db.query(Attendance).filter(
            Attendance.student_id == student_id
        ).all()
        
        if not attendance_records:
            return StudentAttendanceSummary()
        
        total_days = len(attendance_records)
        present_days = sum(1 for a in attendance_records if a.status == "Present")
        absent_days = sum(1 for a in attendance_records if a.status == "Absent")
        leave_days = sum(1 for a in attendance_records if a.status == "Leave")
        
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        return StudentAttendanceSummary(
            total_days=total_days,
            present_days=present_days,
            absent_days=absent_days,
            leave_days=leave_days,
            attendance_percentage=round(attendance_percentage, 2)
        )
    
    @staticmethod
    def get_attendance_details(db: Session, student_id: int, 
                              limit: int = 30) -> List[dict]:
        """
        Get detailed attendance records
        
        Args:
            db: Database session
            student_id: Student ID
            limit: Number of recent records to return
            
        Returns:
            List of attendance records
        """
        records = db.query(Attendance).filter(
            Attendance.student_id == student_id
        ).order_by(Attendance.date.desc()).limit(limit).all()
        
        return [
            {
                "date": r.date.strftime("%d-%m-%Y"),
                "status": r.status,
                "remarks": r.remarks
            }
            for r in records
        ]
    
    @staticmethod
    def get_fee_summary(db: Session, student_id: int) -> StudentFeesSummary:
        """
        Calculate fee summary for a student
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            StudentFeesSummary with fee statistics
        """
        fee_records = db.query(Fee).filter(
            Fee.student_id == student_id
        ).all()
        
        total_fee = sum(f.amount for f in fee_records)
        paid_fee = sum(f.paid_amount for f in fee_records)
        pending_fee = total_fee - paid_fee
        
        fee_percentage = (paid_fee / total_fee * 100) if total_fee > 0 else 0
        
        return StudentFeesSummary(
            total_fee=round(total_fee, 2),
            paid_fee=round(paid_fee, 2),
            pending_fee=round(pending_fee, 2),
            fee_percentage=round(fee_percentage, 2)
        )
    
    @staticmethod
    def get_pending_fees(db: Session, student_id: int) -> List[dict]:
        """
        Get pending fee records
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            List of pending fee records
        """
        records = db.query(Fee).filter(
            Fee.student_id == student_id,
            Fee.status.in_(["Pending", "Partial"])
        ).all()
        
        return [
            {
                "month": r.month,
                "amount": r.amount,
                "paid_amount": r.paid_amount,
                "pending_amount": r.amount - r.paid_amount,
                "status": r.status,
                "due_date": r.due_date.strftime("%d-%m-%Y")
            }
            for r in records
        ]
    
    @staticmethod
    def get_marks_summary(db: Session, student_id: int) -> StudentMarksSummary:
        """
        Calculate marks summary for a student
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            StudentMarksSummary with marks statistics
        """
        mark_records = db.query(Mark).filter(
            Mark.student_id == student_id
        ).all()
        
        if not mark_records:
            return StudentMarksSummary()
        
        total_exams = len(mark_records)
        average_percentage = sum(m.percentage for m in mark_records) / total_exams if mark_records else 0
        total_marks_obtained = sum(m.marks_obtained for m in mark_records)
        total_marks = sum(m.total_marks for m in mark_records)
        
        # Group by subject
        marks_by_subject = {}
        for mark in mark_records:
            if mark.subject not in marks_by_subject:
                marks_by_subject[mark.subject] = {
                    "total_marks": 0,
                    "marks_obtained": 0,
                    "exams": 0,
                    "average_percentage": 0
                }
            
            marks_by_subject[mark.subject]["total_marks"] += mark.total_marks
            marks_by_subject[mark.subject]["marks_obtained"] += mark.marks_obtained
            marks_by_subject[mark.subject]["exams"] += 1
        
        # Calculate average per subject
        for subject, data in marks_by_subject.items():
            if data["total_marks"] > 0:
                data["average_percentage"] = round(
                    (data["marks_obtained"] / data["total_marks"]) * 100, 2
                )
        
        return StudentMarksSummary(
            total_exams=total_exams,
            average_percentage=round(average_percentage, 2),
            total_marks_obtained=round(total_marks_obtained, 2),
            total_marks=round(total_marks, 2),
            marks_by_subject=[
                {"subject": subj, **data}
                for subj, data in marks_by_subject.items()
            ]
        )
    
    @staticmethod
    def get_recent_marks(db: Session, student_id: int, limit: int = 5) -> List[dict]:
        """
        Get recent exam marks
        
        Args:
            db: Database session
            student_id: Student ID
            limit: Number of records
            
        Returns:
            List of mark records
        """
        records = db.query(Mark).filter(
            Mark.student_id == student_id
        ).order_by(Mark.exam_date.desc()).limit(limit).all()
        
        return [
            {
                "exam_name": r.exam_name,
                "subject": r.subject,
                "marks_obtained": r.marks_obtained,
                "total_marks": r.total_marks,
                "percentage": r.percentage,
                "grade": r.grade,
                "exam_date": r.exam_date.strftime("%d-%m-%Y")
            }
            for r in records
        ]
    
    @staticmethod
    def get_pending_homework(db: Session, student_id: int) -> List[dict]:
        """
        Get pending homework assignments
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            List of pending homework
        """
        records = db.query(Homework).filter(
            Homework.student_id == student_id,
            Homework.status.in_(["Assigned", "Submitted"])
        ).order_by(Homework.due_date.asc()).all()
        
        return [
            {
                "subject": r.subject,
                "title": r.title,
                "due_date": r.due_date.strftime("%d-%m-%Y"),
                "status": r.status
            }
            for r in records
        ]
    
    @staticmethod
    def get_homework_summary(db: Session, student_id: int) -> dict:
        """
        Get homework summary
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            Homework statistics
        """
        all_homework = db.query(Homework).filter(
            Homework.student_id == student_id
        ).all()
        
        assigned_count = sum(1 for h in all_homework if h.status == "Assigned")
        submitted_count = sum(1 for h in all_homework if h.status == "Submitted")
        evaluated_count = sum(1 for h in all_homework if h.status == "Evaluated")
        
        avg_marks = 0
        if evaluated_count > 0:
            evaluated_hw = [h for h in all_homework if h.status == "Evaluated" and h.marks_obtained]
            if evaluated_hw:
                avg_marks = sum(h.marks_obtained for h in evaluated_hw) / len(evaluated_hw)
        
        return {
            "assigned": assigned_count,
            "submitted": submitted_count,
            "evaluated": evaluated_count,
            "average_marks": round(avg_marks, 2)
        }
    
    @staticmethod
    def get_comprehensive_profile(db: Session, student_id: int) -> dict:
        """
        Get comprehensive student profile
        
        Args:
            db: Database session
            student_id: Student ID
            
        Returns:
            Complete student profile with all information
        """
        student = StudentService.get_student_by_id(db, student_id)
        
        if not student:
            return None
        
        attendance_summary = StudentService.get_attendance_summary(db, student_id)
        fee_summary = StudentService.get_fee_summary(db, student_id)
        marks_summary = StudentService.get_marks_summary(db, student_id)
        homework_summary = StudentService.get_homework_summary(db, student_id)
        pending_homework = StudentService.get_pending_homework(db, student_id)
        recent_marks = StudentService.get_recent_marks(db, student_id, 5)
        
        return {
            "student": {
                "id": student.id,
                "name": student.name,
                "roll_number": student.roll_number,
                "class": student.class_obj.name if student.class_obj else None,
                "email": student.email
            },
            "attendance": attendance_summary.dict(),
            "fees": fee_summary.dict(),
            "marks": marks_summary.dict(),
            "homework": homework_summary,
            "recent_homework": pending_homework,
            "recent_marks": recent_marks
        }
