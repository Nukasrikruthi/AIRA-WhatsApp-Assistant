"""
Parent service - Handle parent-related business logic
"""
from sqlalchemy.orm import Session
from app.models.models import Parent, Student, ParentSession
from app.schemas.schemas import ParentResponse, StudentResponse
from typing import Optional, List


class ParentService:
    """Service for parent operations"""
    
    @staticmethod
    def get_parent_by_phone(db: Session, phone_number: str) -> Optional[Parent]:
        """
        Get parent by phone number
        
        Args:
            db: Database session
            phone_number: Parent's phone number
            
        Returns:
            Parent object if found, None otherwise
        """
        parent = db.query(Parent).filter(
            Parent.phone_number == phone_number,
            Parent.is_active == True
        ).first()
        return parent
    
    @staticmethod
    def get_parent_by_id(db: Session, parent_id: int) -> Optional[Parent]:
        """Get parent by ID"""
        return db.query(Parent).filter(
            Parent.id == parent_id,
            Parent.is_active == True
        ).first()
    
    @staticmethod
    def get_parent_students(db: Session, parent_id: int) -> List[Student]:
        """
        Get all students of a parent
        
        Args:
            db: Database session
            parent_id: Parent ID
            
        Returns:
            List of student objects
        """
        students = db.query(Student).filter(
            Student.parent_id == parent_id,
            Student.is_active == True
        ).all()
        return students
    
    @staticmethod
    def create_parent(db: Session, phone_number: str, name: str, 
                     email: Optional[str] = None, 
                     alternate_phone: Optional[str] = None) -> Parent:
        """
        Create a new parent
        
        Args:
            db: Database session
            phone_number: Parent's phone number
            name: Parent's name
            email: Parent's email
            alternate_phone: Alternate contact number
            
        Returns:
            Created parent object
        """
        # Check if parent already exists
        existing = db.query(Parent).filter(
            Parent.phone_number == phone_number
        ).first()
        
        if existing:
            return existing
        
        parent = Parent(
            phone_number=phone_number,
            name=name,
            email=email,
            alternate_phone=alternate_phone,
            is_active=True
        )
        db.add(parent)
        db.commit()
        db.refresh(parent)
        return parent
    
    @staticmethod
    def get_or_create_session(db: Session, parent_id: int) -> ParentSession:
        """
        Get or create a session for parent
        
        Args:
            db: Database session
            parent_id: Parent ID
            
        Returns:
            ParentSession object
        """
        session = db.query(ParentSession).filter(
            ParentSession.parent_id == parent_id
        ).first()
        
        if not session:
            session = ParentSession(
                parent_id=parent_id,
                current_menu="main"
            )
            db.add(session)
            db.commit()
            db.refresh(session)
        
        return session
    
    @staticmethod
    def update_session_menu(db: Session, session_id: int, menu: str, 
                           student_id: Optional[int] = None) -> ParentSession:
        """
        Update session menu state
        
        Args:
            db: Database session
            session_id: Session ID
            menu: Current menu state
            student_id: Currently selected student ID
            
        Returns:
            Updated ParentSession object
        """
        session = db.query(ParentSession).filter(
            ParentSession.id == session_id
        ).first()
        
        if session:
            session.current_menu = menu
            if student_id:
                session.current_student_id = student_id
            
            db.commit()
            db.refresh(session)
        
        return session
