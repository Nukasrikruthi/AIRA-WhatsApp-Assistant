"""
WhatsApp service - Handle WhatsApp conversation logic
"""
from sqlalchemy.orm import Session
from app.models.models import Parent, Student
from app.services.parent_service import ParentService
from app.services.student_service import StudentService
from typing import Dict, Optional, List, Tuple


class WhatsAppService:
    """Service for WhatsApp conversation management"""
    
    # Menu states
    MENU_MAIN = "main"
    MENU_STUDENT_SELECT = "student_select"
    MENU_STUDENT_PROFILE = "student_profile"
    MENU_ATTENDANCE_MAIN = "attendance_main"
    MENU_ATTENDANCE_DETAILS = "attendance_details"
    MENU_FEES_MAIN = "fees_main"
    MENU_FEES_DETAILS = "fees_details"
    MENU_MARKS_MAIN = "marks_main"
    MENU_MARKS_DETAILS = "marks_details"
    MENU_HOMEWORK_MAIN = "homework_main"
    MENU_HOMEWORK_DETAILS = "homework_details"
    
    @staticmethod
    def handle_incoming_message(db: Session, phone_number: str, 
                               message_body: str) -> Tuple[str, str]:
        """
        Handle incoming WhatsApp message and return response
        
        Args:
            db: Database session
            phone_number: Sender's phone number
            message_body: Message body
            
        Returns:
            Tuple of (response_message, current_menu)
        """
        # Get parent by phone
        parent = ParentService.get_parent_by_phone(db, phone_number)
        
        if not parent:
            return (
                "Hello! 👋\n\n"
                "Welcome to AIRA Parent Assistant.\n\n"
                "I couldn't find your account associated with this phone number.\n"
                "Please contact the school admin for registration.\n\n"
                "School Contact: +91-XXXXX-XXXXX"
            ), "not_registered"
        
        # Get or create session
        session = ParentService.get_or_create_session(db, parent.id)
        
        # Parse user input
        user_input = message_body.strip().upper()
        
        # Route based on current menu and user input
        response, new_menu = WhatsAppService._route_message(
            db, parent, session, user_input, session.current_menu
        )
        
        # Update session
        if new_menu != session.current_menu:
            ParentService.update_session_menu(db, session.id, new_menu)
        
        return response, new_menu
    
    @staticmethod
    def _route_message(db: Session, parent: Parent, session, 
                      user_input: str, current_menu: str) -> Tuple[str, str]:
        """Route message to appropriate handler"""
        
        if current_menu == WhatsAppService.MENU_MAIN:
            return WhatsAppService._handle_main_menu(db, parent, user_input)
        
        elif current_menu == WhatsAppService.MENU_STUDENT_SELECT:
            return WhatsAppService._handle_student_select(db, parent, session, user_input)
        
        elif current_menu == WhatsAppService.MENU_STUDENT_PROFILE:
            return WhatsAppService._handle_student_profile(db, session, user_input)
        
        elif current_menu == WhatsAppService.MENU_ATTENDANCE_MAIN:
            return WhatsAppService._handle_attendance_menu(db, parent, session, user_input)
        
        elif current_menu == WhatsAppService.MENU_FEES_MAIN:
            return WhatsAppService._handle_fees_menu(db, parent, session, user_input)
        
        elif current_menu == WhatsAppService.MENU_MARKS_MAIN:
            return WhatsAppService._handle_marks_menu(db, parent, session, user_input)
        
        elif current_menu == WhatsAppService.MENU_HOMEWORK_MAIN:
            return WhatsAppService._handle_homework_menu(db, parent, session, user_input)
        
        else:
            return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
    
    @staticmethod
    def _handle_main_menu(db: Session, parent: Parent, user_input: str) -> Tuple[str, str]:
        """Handle main menu selection"""
        
        # If greeting, show welcome
        if user_input in ["HI", "HELLO", "HEY", "START", "MENU", "HELP"]:
            response = WhatsAppService._get_main_menu_with_greeting(parent.name)
            return response, WhatsAppService.MENU_MAIN
        
        # Menu options
        if user_input == "1":
            students = ParentService.get_parent_students(db, parent.id)
            if len(students) == 1:
                return WhatsAppService._get_student_profile_response(db, students[0])
            else:
                return WhatsAppService._get_student_select_response(students), WhatsAppService.MENU_STUDENT_SELECT
        
        elif user_input == "2":
            students = ParentService.get_parent_students(db, parent.id)
            if len(students) == 1:
                return WhatsAppService._get_attendance_response(db, students[0]), WhatsAppService.MENU_ATTENDANCE_MAIN
            else:
                return WhatsAppService._get_student_select_for_attendance(students), WhatsAppService.MENU_ATTENDANCE_MAIN
        
        elif user_input == "3":
            students = ParentService.get_parent_students(db, parent.id)
            if len(students) == 1:
                return WhatsAppService._get_fees_response(db, students[0]), WhatsAppService.MENU_FEES_MAIN
            else:
                return WhatsAppService._get_student_select_for_fees(students), WhatsAppService.MENU_FEES_MAIN
        
        elif user_input == "4":
            students = ParentService.get_parent_students(db, parent.id)
            if len(students) == 1:
                return WhatsAppService._get_marks_response(db, students[0]), WhatsAppService.MENU_MARKS_MAIN
            else:
                return WhatsAppService._get_student_select_for_marks(students), WhatsAppService.MENU_MARKS_MAIN
        
        elif user_input == "5":
            students = ParentService.get_parent_students(db, parent.id)
            if len(students) == 1:
                return WhatsAppService._get_homework_response(db, students[0]), WhatsAppService.MENU_HOMEWORK_MAIN
            else:
                return WhatsAppService._get_student_select_for_homework(students), WhatsAppService.MENU_HOMEWORK_MAIN
        
        else:
            return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
    
    @staticmethod
    def _handle_student_select(db: Session, parent: Parent, session, 
                              user_input: str) -> Tuple[str, str]:
        """Handle student selection"""
        
        students = ParentService.get_parent_students(db, parent.id)
        
        try:
            student_idx = int(user_input) - 1
            if 0 <= student_idx < len(students):
                student = students[student_idx]
                ParentService.update_session_menu(db, session.id, 
                                                 WhatsAppService.MENU_STUDENT_PROFILE, 
                                                 student.id)
                return WhatsAppService._get_student_profile_response(db, student), WhatsAppService.MENU_STUDENT_PROFILE
        except ValueError:
            pass
        
        return WhatsAppService._get_student_select_response(students), WhatsAppService.MENU_STUDENT_SELECT
    
    @staticmethod
    def _handle_student_profile(db: Session, session, user_input: str) -> Tuple[str, str]:
        """Handle student profile menu"""
        
        student_id = session.current_student_id
        if not student_id:
            return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        if user_input == "0":
            return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        return WhatsAppService._get_student_profile_response(db, 
            StudentService.get_student_by_id(db, student_id)), WhatsAppService.MENU_STUDENT_PROFILE
    
    @staticmethod
    def _handle_attendance_menu(db: Session, parent: Parent, session, 
                               user_input: str) -> Tuple[str, str]:
        """Handle attendance menu"""
        
        students = ParentService.get_parent_students(db, parent.id)
        
        try:
            student_idx = int(user_input) - 1
            if 0 <= student_idx < len(students):
                student = students[student_idx]
                return WhatsAppService._get_attendance_details_response(db, student), WhatsAppService.MENU_ATTENDANCE_DETAILS
        except ValueError:
            if user_input == "0":
                return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        return WhatsAppService._get_attendance_response(db, students[0] if students else None), WhatsAppService.MENU_ATTENDANCE_MAIN
    
    @staticmethod
    def _handle_fees_menu(db: Session, parent: Parent, session, 
                         user_input: str) -> Tuple[str, str]:
        """Handle fees menu"""
        
        students = ParentService.get_parent_students(db, parent.id)
        
        try:
            student_idx = int(user_input) - 1
            if 0 <= student_idx < len(students):
                student = students[student_idx]
                return WhatsAppService._get_fees_details_response(db, student), WhatsAppService.MENU_FEES_DETAILS
        except ValueError:
            if user_input == "0":
                return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        return WhatsAppService._get_fees_response(db, students[0] if students else None), WhatsAppService.MENU_FEES_MAIN
    
    @staticmethod
    def _handle_marks_menu(db: Session, parent: Parent, session, 
                          user_input: str) -> Tuple[str, str]:
        """Handle marks menu"""
        
        students = ParentService.get_parent_students(db, parent.id)
        
        try:
            student_idx = int(user_input) - 1
            if 0 <= student_idx < len(students):
                student = students[student_idx]
                return WhatsAppService._get_marks_details_response(db, student), WhatsAppService.MENU_MARKS_DETAILS
        except ValueError:
            if user_input == "0":
                return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        return WhatsAppService._get_marks_response(db, students[0] if students else None), WhatsAppService.MENU_MARKS_MAIN
    
    @staticmethod
    def _handle_homework_menu(db: Session, parent: Parent, session, 
                             user_input: str) -> Tuple[str, str]:
        """Handle homework menu"""
        
        students = ParentService.get_parent_students(db, parent.id)
        
        try:
            student_idx = int(user_input) - 1
            if 0 <= student_idx < len(students):
                student = students[student_idx]
                return WhatsAppService._get_homework_details_response(db, student), WhatsAppService.MENU_HOMEWORK_DETAILS
        except ValueError:
            if user_input == "0":
                return WhatsAppService._get_main_menu(), WhatsAppService.MENU_MAIN
        
        return WhatsAppService._get_homework_response(db, students[0] if students else None), WhatsAppService.MENU_HOMEWORK_MAIN
    
    # Response formatters
    @staticmethod
    def _get_main_menu() -> str:
        """Get main menu response"""
        return (
            "Welcome to AIRA Parent Assistant! 👋\n\n"
            "Please select an option:\n\n"
            "1️⃣  Student Profile\n"
            "2️⃣  Attendance\n"
            "3️⃣  Fee Details\n"
            "4️⃣  Marks\n"
            "5️⃣  Homework\n\n"
            "Reply with the number of your choice."
        )
    
    @staticmethod
    def _get_main_menu_with_greeting(name: str) -> str:
        """Get greeting and main menu"""
        return (
            f"Hello {name}! 👋\n\n"
            "Welcome to AIRA Parent Assistant.\n\n"
            "Please select an option:\n\n"
            "1️⃣  Student Profile\n"
            "2️⃣  Attendance\n"
            "3️⃣  Fee Details\n"
            "4️⃣  Marks\n"
            "5️⃣  Homework\n\n"
            "Reply with the number of your choice."
        )
    
    @staticmethod
    def _get_student_select_response(students: List[Student]) -> str:
        """Get student selection response"""
        response = "Please select a student:\n\n"
        for idx, student in enumerate(students, 1):
            response += f"{idx}️⃣  {student.name} (Class {student.class_obj.name})\n"
        response += "\nReply with the number."
        return response
    
    @staticmethod
    def _get_student_select_for_attendance(students: List[Student]) -> str:
        """Get student selection for attendance"""
        response = "Select student for attendance:\n\n"
        for idx, student in enumerate(students, 1):
            response += f"{idx}️⃣  {student.name}\n"
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_student_select_for_fees(students: List[Student]) -> str:
        """Get student selection for fees"""
        response = "Select student for fee details:\n\n"
        for idx, student in enumerate(students, 1):
            response += f"{idx}️⃣  {student.name}\n"
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_student_select_for_marks(students: List[Student]) -> str:
        """Get student selection for marks"""
        response = "Select student for marks:\n\n"
        for idx, student in enumerate(students, 1):
            response += f"{idx}️⃣  {student.name}\n"
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_student_select_for_homework(students: List[Student]) -> str:
        """Get student selection for homework"""
        response = "Select student for homework:\n\n"
        for idx, student in enumerate(students, 1):
            response += f"{idx}️⃣  {student.name}\n"
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_student_profile_response(db: Session, student: Student) -> Tuple[str, str]:
        """Get student profile response"""
        if not student:
            return "Student not found.", WhatsAppService.MENU_MAIN
        
        profile = StudentService.get_comprehensive_profile(db, student.id)
        
        response = (
            f"📚 {student.name.upper()} - Student Profile\n\n"
            f"Class: {student.class_obj.name if student.class_obj else 'N/A'}\n"
            f"Roll Number: {student.roll_number}\n"
            f"Email: {student.email}\n\n"
        )
        
        # Attendance
        att = profile['attendance']
        response += f"📊 ATTENDANCE: {att['attendance_percentage']}%\n"
        response += f"Present: {att['present_days']}/{att['total_days']} days\n\n"
        
        # Fees
        fees = profile['fees']
        response += f"💰 FEE STATUS: ₹{fees['pending_fee']} Pending\n"
        response += f"Paid: ₹{fees['paid_fee']} / ₹{fees['total_fee']}\n\n"
        
        # Marks
        marks = profile['marks']
        response += f"📈 MARKS: {marks['average_percentage']}% Average\n"
        response += f"Total Exams: {marks['total_exams']}\n\n"
        
        # Homework
        hw = profile['homework']
        response += f"📝 HOMEWORK:\n"
        response += f"Assigned: {hw['assigned']}, Submitted: {hw['submitted']}, Evaluated: {hw['evaluated']}\n\n"
        
        response += (
            "0️⃣  Back to Main Menu\n\n"
            "Reply with 0 to go back."
        )
        
        return response, WhatsAppService.MENU_STUDENT_PROFILE
    
    @staticmethod
    def _get_attendance_response(db: Session, student: Student) -> str:
        """Get attendance response"""
        if not student:
            return "No student found."
        
        summary = StudentService.get_attendance_summary(db, student.id)
        
        return (
            f"📊 {student.name} - Attendance\n\n"
            f"Attendance Percentage: {summary.attendance_percentage}%\n"
            f"Present Days: {summary.present_days}\n"
            f"Absent Days: {summary.absent_days}\n"
            f"Leave Days: {summary.leave_days}\n"
            f"Total Days: {summary.total_days}\n\n"
            "0️⃣  Back to Main Menu"
        )
    
    @staticmethod
    def _get_attendance_details_response(db: Session, student: Student) -> str:
        """Get detailed attendance"""
        if not student:
            return "No student found."
        
        details = StudentService.get_attendance_details(db, student.id, 10)
        
        response = f"📊 {student.name} - Recent Attendance\n\n"
        for record in details:
            emoji = "✅" if record['status'] == "Present" else "❌" if record['status'] == "Absent" else "📋"
            response += f"{emoji} {record['date']} - {record['status']}\n"
        
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_fees_response(db: Session, student: Student) -> str:
        """Get fees response"""
        if not student:
            return "No student found."
        
        summary = StudentService.get_fee_summary(db, student.id)
        pending = StudentService.get_pending_fees(db, student.id)
        
        response = f"💰 {student.name} - Fee Details\n\n"
        response += f"Total Fee: ₹{summary.total_fee}\n"
        response += f"Paid: ₹{summary.paid_fee}\n"
        response += f"Pending: ₹{summary.pending_fee}\n\n"
        
        if pending:
            response += "Pending Fees:\n"
            for fee in pending[:3]:  # Show first 3
                response += f"• {fee['month']}: ₹{fee['pending_amount']} (Due: {fee['due_date']})\n"
        
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_fees_details_response(db: Session, student: Student) -> str:
        """Get detailed fees"""
        if not student:
            return "No student found."
        
        pending = StudentService.get_pending_fees(db, student.id)
        
        response = f"💰 {student.name} - Pending Fees\n\n"
        
        if pending:
            for fee in pending:
                response += f"Month: {fee['month']}\n"
                response += f"Amount: ₹{fee['amount']}\n"
                response += f"Paid: ₹{fee['paid_amount']}\n"
                response += f"Pending: ₹{fee['pending_amount']}\n"
                response += f"Due Date: {fee['due_date']}\n\n"
        else:
            response += "No pending fees! ✅\n\n"
        
        response += "0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_marks_response(db: Session, student: Student) -> str:
        """Get marks response"""
        if not student:
            return "No student found."
        
        summary = StudentService.get_marks_summary(db, student.id)
        recent = StudentService.get_recent_marks(db, student.id, 3)
        
        response = f"📈 {student.name} - Marks\n\n"
        response += f"Average: {summary.average_percentage}%\n"
        response += f"Total Exams: {summary.total_exams}\n\n"
        
        response += "Recent Exams:\n"
        for mark in recent:
            response += f"• {mark['exam_name']} - {mark['subject']}: {mark['percentage']}% ({mark['grade']})\n"
        
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_marks_details_response(db: Session, student: Student) -> str:
        """Get detailed marks"""
        if not student:
            return "No student found."
        
        recent = StudentService.get_recent_marks(db, student.id, 10)
        
        response = f"📈 {student.name} - All Marks\n\n"
        for mark in recent:
            response += f"{mark['exam_name']} - {mark['subject']}\n"
            response += f"Marks: {mark['marks_obtained']}/{mark['total_marks']}\n"
            response += f"Percentage: {mark['percentage']}% ({mark['grade']})\n"
            response += f"Date: {mark['exam_date']}\n\n"
        
        response += "0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_homework_response(db: Session, student: Student) -> str:
        """Get homework response"""
        if not student:
            return "No student found."
        
        summary = StudentService.get_homework_summary(db, student.id)
        pending = StudentService.get_pending_homework(db, student.id)
        
        response = f"📝 {student.name} - Homework\n\n"
        response += f"Assigned: {summary['assigned']}\n"
        response += f"Submitted: {summary['submitted']}\n"
        response += f"Evaluated: {summary['evaluated']}\n\n"
        
        if pending:
            response += "Pending Assignments:\n"
            for hw in pending[:3]:
                response += f"• {hw['subject']}: {hw['title']}\n"
                response += f"  Due: {hw['due_date']}\n"
        
        response += "\n0️⃣  Back to Main Menu"
        return response
    
    @staticmethod
    def _get_homework_details_response(db: Session, student: Student) -> str:
        """Get detailed homework"""
        if not student:
            return "No student found."
        
        pending = StudentService.get_pending_homework(db, student.id)
        
        response = f"📝 {student.name} - Pending Homework\n\n"
        
        if pending:
            for hw in pending:
                response += f"Subject: {hw['subject']}\n"
                response += f"Task: {hw['title']}\n"
                response += f"Due Date: {hw['due_date']}\n"
                response += f"Status: {hw['status']}\n\n"
        else:
            response += "No pending homework! ✅\n\n"
        
        response += "0️⃣  Back to Main Menu"
        return response
