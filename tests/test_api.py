"""
Unit tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from app.database.engine import SessionLocal
from app.models.models import Base, Parent, Class, Student, Attendance, Fee, Mark, Homework
from datetime import date, timedelta
import random

# Create test client
client = TestClient(app)


@pytest.fixture(scope="session")
def db():
    """Create test database"""
    Base.metadata.create_all(bind=SessionLocal.kw['bind'])
    db_session = SessionLocal()
    yield db_session
    db_session.close()


@pytest.fixture
def setup_test_data(db):
    """Setup test data"""
    # Create test data
    # Clear existing data
    db.query(Mark).delete()
    db.query(Homework).delete()
    db.query(Fee).delete()
    db.query(Attendance).delete()
    db.query(Student).delete()
    db.query(Parent).delete()
    db.query(Class).delete()
    
    # Create class
    test_class = Class(name="8A")
    db.add(test_class)
    db.flush()
    
    # Create parent
    parent = Parent(
        phone_number="+6302894103",
        name="Test Parent",
        email="parent@test.com"
    )
    db.add(parent)
    db.flush()
    
    # Create student
    student = Student(
        name="Test Student",
        roll_number="001",
        parent_id=parent.id,
        class_id=test_class.id,
        email="student@test.com"
    )
    db.add(student)
    db.flush()
    
    # Create attendance record
    attendance = Attendance(
        student_id=student.id,
        date=date.today(),
        status="Present"
    )
    db.add(attendance)
    
    # Create fee record
    fee = Fee(
        student_id=student.id,
        month="01-2024",
        amount=5000,
        paid_amount=5000,
        status="Paid",
        due_date=date(2024, 1, 15),
        payment_date=date(2024, 1, 10)
    )
    db.add(fee)
    
    # Create homework record
    homework = Homework(
        student_id=student.id,
        subject="Math",
        title="Test Homework",
        description="Test homework description",
        due_date=date.today() + timedelta(days=5),
        assigned_date=date.today(),
        status="Assigned"
    )
    db.add(homework)
    
    # Create mark record
    mark = Mark(
        student_id=student.id,
        exam_name="Unit Test 1",
        subject="Math",
        marks_obtained=85,
        total_marks=100,
        percentage=85,
        grade="A",
        exam_date=date.today()
    )
    db.add(mark)
    
    db.commit()
    
    return {
        "parent": parent,
        "student": student,
        "class": test_class
    }


class TestHealth:
    """Test health endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestParentAPI:
    """Test parent API endpoints"""
    
    def test_get_parent_not_found(self):
        """Test getting non-existent parent"""
        response = client.get("/api/parents/+9999999999")
        assert response.status_code == 404
    
    def test_create_parent(self):
        """Test creating a parent"""
        response = client.post(
            "/api/parents/",
            params={
                "phone_number": "+1234567890",
                "name": "New Parent",
                "email": "newparent@test.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Parent"
        assert data["phone_number"] == "+1234567890"


class TestStudentAPI:
    """Test student API endpoints"""
    
    def test_get_student_not_found(self):
        """Test getting non-existent student"""
        response = client.get("/api/students/9999")
        assert response.status_code == 404
    
    def test_get_student_profile(self, setup_test_data):
        """Test getting student profile"""
        student = setup_test_data["student"]
        response = client.get(f"/api/students/{student.id}/profile")
        assert response.status_code == 200
        data = response.json()
        assert data["student"]["name"] == "Test Student"
        assert "attendance" in data
        assert "fees" in data
        assert "marks" in data
    
    def test_get_student_attendance(self, setup_test_data):
        """Test getting attendance"""
        student = setup_test_data["student"]
        response = client.get(f"/api/students/{student.id}/attendance")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "recent_records" in data
    
    def test_get_student_fees(self, setup_test_data):
        """Test getting fees"""
        student = setup_test_data["student"]
        response = client.get(f"/api/students/{student.id}/fees")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "pending_fees" in data
    
    def test_get_student_marks(self, setup_test_data):
        """Test getting marks"""
        student = setup_test_data["student"]
        response = client.get(f"/api/students/{student.id}/marks")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "recent_marks" in data
    
    def test_get_student_homework(self, setup_test_data):
        """Test getting homework"""
        student = setup_test_data["student"]
        response = client.get(f"/api/students/{student.id}/homework")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "pending_homework" in data


class TestWhatsAppWebhook:
    """Test WhatsApp webhook"""
    
    def test_whatsapp_webhook_unregistered_user(self):
        """Test webhook with unregistered user"""
        response = client.post(
            "/api/whatsapp/webhook",
            data={
                "From": "whatsapp:+9999999999",
                "Body": "Hi",
                "MessageSid": "test-sid"
            }
        )
        assert response.status_code == 200
        data = response.json()
        # Should handle gracefully
        assert "status" in data
    
    def test_whatsapp_webhook_registered_user(self, setup_test_data):
        """Test webhook with registered user"""
        parent = setup_test_data["parent"]
        response = client.post(
            "/api/whatsapp/webhook",
            data={
                "From": f"whatsapp:{parent.phone_number}",
                "Body": "Hi",
                "MessageSid": "test-sid"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["success", "error"]


class TestAttendanceAPI:
    """Test attendance endpoints"""
    
    def test_get_attendance(self, setup_test_data):
        """Test getting attendance"""
        student = setup_test_data["student"]
        response = client.get(f"/api/attendance/student/{student.id}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "recent_records" in data


class TestFeesAPI:
    """Test fees endpoints"""
    
    def test_get_fees(self, setup_test_data):
        """Test getting fees"""
        student = setup_test_data["student"]
        response = client.get(f"/api/fees/student/{student.id}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "pending_fees" in data


class TestMarksAPI:
    """Test marks endpoints"""
    
    def test_get_marks(self, setup_test_data):
        """Test getting marks"""
        student = setup_test_data["student"]
        response = client.get(f"/api/marks/student/{student.id}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "recent_marks" in data


class TestHomeworkAPI:
    """Test homework endpoints"""
    
    def test_get_homework(self, setup_test_data):
        """Test getting homework"""
        student = setup_test_data["student"]
        response = client.get(f"/api/homework/student/{student.id}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "pending_homework" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
