"""
Dummy Data Generation Script for AIRA Database

This script creates realistic dummy data for MVP testing:
- 10 Parents
- 20 Students (2-3 per parent)
- Attendance records (130 days per student)
- Fee records (12 months)
- Homework assignments (10 per student)
- Exam marks (4 exams × 5 subjects per student)

Run this script to populate the database with test data.
"""

from datetime import datetime, date, timedelta
import random
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.engine import engine, SessionLocal
from app.models.models import (
    Base, Parent, Class, Student, Attendance, Fee, Homework, Mark, ParentSession
)


# Sample Data
PARENT_DATA = [
    {"phone": "+6302894103", "name": "Rajesh Sharma", "email": "rajesh.sharma@email.com"},
    {"phone": "+6312456789", "name": "Priya Desai", "email": "priya.desai@email.com"},
    {"phone": "+6323456789", "name": "Amit Patel", "email": "amit.patel@email.com"},
    {"phone": "+6334567890", "name": "Neha Gupta", "email": "neha.gupta@email.com"},
    {"phone": "+6345678901", "name": "Vikram Singh", "email": "vikram.singh@email.com"},
    {"phone": "+6356789012", "name": "Anjali Kumar", "email": "anjali.kumar@email.com"},
    {"phone": "+6367890123", "name": "Sanjay Verma", "email": "sanjay.verma@email.com"},
    {"phone": "+6378901234", "name": "Meera Nair", "email": "meera.nair@email.com"},
    {"phone": "+6389012345", "name": "Akshay Reddy", "email": "akshay.reddy@email.com"},
    {"phone": "+6390123456", "name": "Divya Iyer", "email": "divya.iyer@email.com"},
]

CLASS_DATA = [
    "5", "5B", "6", "6B", "7", "7B", "8", "8B", "9", "9B", "10", "11 Science", "11 Commerce", "12 Science"
]

STUDENT_FIRST_NAMES = [
    "Rahul", "Priya", "Arjun", "Anaya", "Rohan", "Aditya", "Isha", "Vivek",
    "Shreya", "Nikhil", "Pooja", "Aryan", "Zara", "Karan", "Ananya", "Varun",
    "Neha", "Sahil", "Diya", "Sarthak"
]

SUBJECTS = ["Mathematics", "English", "Science", "Social Studies", "Hindi"]

EXAM_TYPES = ["Unit Test 1", "Unit Test 2", "Mid Term", "Final"]

HOMEWORK_TITLES = [
    "Chapter 5 Exercises", "Essay on Environment", "Project on Solar System",
    "Problem Set", "Grammar Exercises", "Math Assignment", "Science Lab Report",
    "History Research", "Art Project", "Reading Comprehension"
]

HOMEWORK_DESCRIPTIONS = {
    "Chapter 5 Exercises": "Complete all exercises from Chapter 5 in the textbook",
    "Essay on Environment": "Write a 500-word essay on environmental conservation",
    "Project on Solar System": "Create a model or presentation of the solar system",
    "Problem Set": "Solve all problems in the problem set provided in class",
    "Grammar Exercises": "Complete grammar exercises from the worksheet",
    "Math Assignment": "Solve 20 math problems from the assignment sheet",
    "Science Lab Report": "Write a report on the conducted lab experiment",
    "History Research": "Research and write about the assigned historical period",
    "Art Project": "Create an art piece based on the given theme",
    "Reading Comprehension": "Read the passage and answer the comprehension questions"
}


def create_classes(db):
    """Create class records"""
    print("Creating classes...")
    for class_name in CLASS_DATA:
        existing = db.query(Class).filter(Class.name == class_name).first()
        if not existing:
            class_obj = Class(name=class_name)
            db.add(class_obj)
    db.commit()
    print(f"✓ Created {len(CLASS_DATA)} classes")


def create_parents(db):
    """Create parent records"""
    print("\nCreating parents...")
    for parent_data in PARENT_DATA:
        existing = db.query(Parent).filter(
            Parent.phone_number == parent_data["phone"]
        ).first()
        if not existing:
            parent = Parent(
                phone_number=parent_data["phone"],
                name=parent_data["name"],
                email=parent_data["email"],
                alternate_phone=None,
                is_active=True
            )
            db.add(parent)
    db.commit()
    print(f"✓ Created {len(PARENT_DATA)} parents")


def create_students(db):
    """Create student records (2-3 per parent)"""
    print("\nCreating students...")
    parents = db.query(Parent).all()
    classes = db.query(Class).all()
    
    student_count = 0
    roll_counter = 1
    
    for parent in parents:
        # 2-3 students per parent
        num_students = random.randint(2, 3)
        for _ in range(num_students):
            student_class = random.choice(classes)
            student_name = random.choice(STUDENT_FIRST_NAMES)
            
            # Ensure unique roll number
            existing_roll = db.query(Student).filter(
                Student.roll_number == f"{roll_counter:03d}"
            ).first()
            
            while existing_roll:
                roll_counter += 1
                existing_roll = db.query(Student).filter(
                    Student.roll_number == f"{roll_counter:03d}"
                ).first()
            
            student = Student(
                name=student_name,
                roll_number=f"{roll_counter:03d}",
                parent_id=parent.id,
                class_id=student_class.id,
                email=f"{student_name.lower()}.student@school.com",
                is_active=True
            )
            db.add(student)
            student_count += 1
            roll_counter += 1
    
    db.commit()
    print(f"✓ Created {student_count} students")


def create_attendance(db):
    """Create attendance records (130 days per student)"""
    print("\nCreating attendance records...")
    students = db.query(Student).all()
    
    attendance_count = 0
    start_date = date(2024, 1, 1)
    
    for student in students:
        # Create 130 attendance records (roughly 6 months)
        for day in range(130):
            attendance_date = start_date + timedelta(days=day)
            
            # Skip weekends (Saturday=5, Sunday=6)
            if attendance_date.weekday() >= 5:
                continue
            
            # Random status with probability: 85% Present, 10% Absent, 5% Leave
            rand = random.random()
            if rand < 0.85:
                status = "Present"
                remarks = None
            elif rand < 0.95:
                status = "Absent"
                remarks = random.choice(["Sick", "Family work", None])
            else:
                status = "Leave"
                remarks = random.choice(["Medical leave", "Family event", "Other"])
            
            attendance = Attendance(
                student_id=student.id,
                date=attendance_date,
                status=status,
                remarks=remarks
            )
            db.add(attendance)
            attendance_count += 1
    
    db.commit()
    print(f"✓ Created {attendance_count} attendance records")


def create_fees(db):
    """Create fee records (12 months per student)"""
    print("\nCreating fee records...")
    students = db.query(Student).all()
    
    fee_count = 0
    fee_amount = 5000  # ₹5000 monthly fee
    
    for student in students:
        for month_num in range(1, 13):
            month_str = f"{month_num:02d}-2024"
            
            # Random fee status distribution: 60% Paid, 20% Pending, 20% Partial
            rand = random.random()
            if rand < 0.60:
                status = "Paid"
                paid_amount = fee_amount
                payment_date = date(2024, month_num, random.randint(1, 15))
            elif rand < 0.80:
                status = "Pending"
                paid_amount = 0
                payment_date = None
            else:
                status = "Partial"
                paid_amount = random.randint(int(fee_amount * 0.4), int(fee_amount * 0.8))
                payment_date = None
            
            due_date = date(2024, month_num, 15)
            
            fee = Fee(
                student_id=student.id,
                month=month_str,
                amount=fee_amount,
                paid_amount=paid_amount,
                status=status,
                due_date=due_date,
                payment_date=payment_date,
                remarks=None if status == "Paid" else random.choice([
                    "Awaiting payment", "Payment pending", "Partially paid", None
                ])
            )
            db.add(fee)
            fee_count += 1
    
    db.commit()
    print(f"✓ Created {fee_count} fee records")


def create_homework(db):
    """Create homework records (~10 per student)"""
    print("\nCreating homework records...")
    students = db.query(Student).all()
    
    homework_count = 0
    
    for student in students:
        # Create 10 homework assignments per student
        for hw_num in range(10):
            assigned_date = date(2024, 1, 1) + timedelta(days=hw_num * 7)
            due_date = assigned_date + timedelta(days=random.randint(3, 7))
            
            title = random.choice(HOMEWORK_TITLES)
            subject = random.choice(SUBJECTS)
            
            # Random status: 40% Submitted, 30% Assigned, 30% Evaluated
            rand = random.random()
            if rand < 0.40:
                status = "Submitted"
                marks_obtained = None
            elif rand < 0.70:
                status = "Assigned"
                marks_obtained = None
            else:
                status = "Evaluated"
                marks_obtained = random.uniform(60, 100)
            
            homework = Homework(
                student_id=student.id,
                subject=subject,
                title=title,
                description=HOMEWORK_DESCRIPTIONS.get(title, "Complete the assignment"),
                due_date=due_date,
                assigned_date=assigned_date,
                status=status,
                marks_obtained=marks_obtained,
                total_marks=100
            )
            db.add(homework)
            homework_count += 1
    
    db.commit()
    print(f"✓ Created {homework_count} homework records")


def create_marks(db):
    """Create exam mark records (~20 per student: 4 exams × 5 subjects)"""
    print("\nCreating exam marks...")
    students = db.query(Student).all()
    
    marks_count = 0
    
    for student in students:
        for exam_idx, exam_name in enumerate(EXAM_TYPES):
            exam_date = date(2024, 1, 1) + timedelta(days=exam_idx * 45)
            
            for subject in SUBJECTS:
                # Random marks: between 40 and 100
                marks_obtained = random.uniform(40, 100)
                total_marks = 100
                percentage = (marks_obtained / total_marks) * 100
                
                # Determine grade
                if percentage >= 90:
                    grade = "A"
                elif percentage >= 80:
                    grade = "B"
                elif percentage >= 70:
                    grade = "C"
                elif percentage >= 60:
                    grade = "D"
                else:
                    grade = "F"
                
                mark = Mark(
                    student_id=student.id,
                    exam_name=exam_name,
                    subject=subject,
                    marks_obtained=round(marks_obtained, 2),
                    total_marks=total_marks,
                    percentage=round(percentage, 2),
                    grade=grade,
                    exam_date=exam_date
                )
                db.add(mark)
                marks_count += 1
    
    db.commit()
    print(f"✓ Created {marks_count} mark records")


def create_sessions(db):
    """Create parent session records"""
    print("\nCreating parent sessions...")
    parents = db.query(Parent).all()
    
    for parent in parents:
        # Get one of parent's students
        student = db.query(Student).filter(
            Student.parent_id == parent.id
        ).first()
        
        session = ParentSession(
            parent_id=parent.id,
            current_student_id=student.id if student else None,
            current_menu="main",
            session_data=None
        )
        db.add(session)
    
    db.commit()
    print(f"✓ Created {len(parents)} parent sessions")


def clear_database(db):
    """Delete all existing data"""
    print("Clearing existing database...")
    
    # Order matters due to foreign keys
    db.query(ParentSession).delete()
    db.query(Mark).delete()
    db.query(Homework).delete()
    db.query(Fee).delete()
    db.query(Attendance).delete()
    db.query(Student).delete()
    db.query(Parent).delete()
    db.query(Class).delete()
    
    db.commit()
    print("✓ Database cleared")


def main():
    """Main function to generate all dummy data"""
    
    print("=" * 60)
    print("AIRA Dummy Data Generation Script")
    print("=" * 60)
    
    # Create database tables
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Create all dummy data
        create_classes(db)
        create_parents(db)
        create_students(db)
        create_attendance(db)
        create_fees(db)
        create_homework(db)
        create_marks(db)
        create_sessions(db)
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        print(f"Parents:            {db.query(Parent).count()}")
        print(f"Classes:            {db.query(Class).count()}")
        print(f"Students:           {db.query(Student).count()}")
        print(f"Attendance Records: {db.query(Attendance).count()}")
        print(f"Fee Records:        {db.query(Fee).count()}")
        print(f"Homework Records:   {db.query(Homework).count()}")
        print(f"Mark Records:       {db.query(Mark).count()}")
        print(f"Parent Sessions:    {db.query(ParentSession).count()}")
        
        print("\n" + "=" * 60)
        print("✓ Dummy data generation completed successfully!")
        print("=" * 60)
        
        # Print sample data for verification
        print("\n" + "=" * 60)
        print("SAMPLE DATA - First Parent and Students")
        print("=" * 60)
        
        parent = db.query(Parent).first()
        if parent:
            print(f"\nParent: {parent.name}")
            print(f"Phone: {parent.phone_number}")
            print(f"Email: {parent.email}")
            
            students = db.query(Student).filter(
                Student.parent_id == parent.id
            ).all()
            
            for student in students:
                print(f"\n  Student: {student.name}")
                print(f"  Roll Number: {student.roll_number}")
                print(f"  Class: {student.class_obj.name if student.class_obj else 'N/A'}")
                
                # Attendance stats
                attendance = db.query(Attendance).filter(
                    Attendance.student_id == student.id,
                    Attendance.status == "Present"
                ).count()
                total_attendance = db.query(Attendance).filter(
                    Attendance.student_id == student.id
                ).count()
                
                if total_attendance > 0:
                    attendance_pct = (attendance / total_attendance) * 100
                    print(f"  Attendance: {attendance_pct:.1f}% ({attendance}/{total_attendance})")
                
                # Fee status
                pending_fee = db.query(Fee).filter(
                    Fee.student_id == student.id,
                    Fee.status.in_(["Pending", "Partial"])
                ).with_entities(Fee.amount - Fee.paid_amount).all()
                
                total_pending = sum([f[0] for f in pending_fee])
                print(f"  Pending Fee: ₹{total_pending}")
                
                # Recent marks
                recent_mark = db.query(Mark).filter(
                    Mark.student_id == student.id
                ).order_by(Mark.exam_date.desc()).first()
                
                if recent_mark:
                    print(f"  Latest Mark: {recent_mark.exam_name} - {recent_mark.percentage:.1f}%")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during data generation: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
