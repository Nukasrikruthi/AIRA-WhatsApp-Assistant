"""
Parent API routes
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database.engine import get_db
from app.schemas.schemas import ParentResponse, ParentDetailResponse, StudentResponse
from app.services.parent_service import ParentService
from typing import List

router = APIRouter(prefix="/api/parents", tags=["Parents"])


@router.get("/{phone_number}", response_model=ParentResponse)
async def get_parent(phone_number: str, db: Session = Depends(get_db)):
    """
    Get parent by phone number
    
    Args:
        phone_number: Parent's WhatsApp phone number
        
    Returns:
        Parent information
    """
    parent = ParentService.get_parent_by_phone(db, phone_number)
    
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    return parent


@router.get("/{parent_id}/students", response_model=List[StudentResponse])
async def get_parent_students(parent_id: int, db: Session = Depends(get_db)):
    """
    Get all students of a parent
    
    Args:
        parent_id: Parent ID
        
    Returns:
        List of students
    """
    parent = ParentService.get_parent_by_id(db, parent_id)
    
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    students = ParentService.get_parent_students(db, parent_id)
    
    return students


@router.post("/", response_model=ParentResponse)
async def create_parent(
    phone_number: str,
    name: str,
    email: str = None,
    alternate_phone: str = None,
    db: Session = Depends(get_db)
):
    """
    Create a new parent (Admin endpoint)
    
    Args:
        phone_number: Parent's phone number
        name: Parent's name
        email: Parent's email
        alternate_phone: Alternate contact
        
    Returns:
        Created parent
    """
    parent = ParentService.create_parent(
        db,
        phone_number=phone_number,
        name=name,
        email=email,
        alternate_phone=alternate_phone
    )
    
    return parent
