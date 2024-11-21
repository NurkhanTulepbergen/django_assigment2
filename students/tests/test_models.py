import pytest
from students.models import Student
import django
from django.conf import settings

# Ensure that Django settings are configured before any tests
settings.configure(default_settings='StudentManagementSystem.settings')
django.setup()

@pytest.mark.django_db
def test_create_student():
    student = Student.objects.create(
        name="John Doe",
        email="john.doe@example.com",
        dob="2000-01-01",
        registration_date="2024-01-01"
    )
    assert student.name == "John Doe"
    assert student.email == "john.doe@example.com"





@pytest.mark.django_db
def test_student_view_permissions():
    client = APIClient()

    # Create a test student user
    student_user = User.objects.create_user(username="student", password="test123")
    student_user.profile.role = "Student"
    student_user.profile.save()

    # Authenticate as the student
    client.login(username="student", password="test123")

    # Test GET endpoint
    response = client.get("/api/students/")
    assert response.status_code == 200  # Should allow access

    # Test POST endpoint (should be restricted for students)
    response = client.post("/api/students/", {"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 403  # Permission denied
