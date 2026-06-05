"""
API routes initialization
"""
from fastapi import APIRouter
from app.api.routes import whatsapp, parent, student, attendance, fees, marks, homework

# Create main router
api_router = APIRouter()

# Include all route modules
api_router.include_router(whatsapp.router)
api_router.include_router(parent.router)
api_router.include_router(student.router)
api_router.include_router(attendance.router)
api_router.include_router(fees.router)
api_router.include_router(marks.router)
api_router.include_router(homework.router)
