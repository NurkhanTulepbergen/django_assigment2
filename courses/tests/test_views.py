import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import django
from django.conf import settings

# Ensure that Django settings are configured before any tests
settings.configure(default_settings='StudentManagementSystem.settings')
django.setup()
@pytest.mark.django_db
def test_course_enrollment():
    client = APIClient()

    # Create test users
    teacher_user = User.objects.create_user(username="teacher", password="test123")
    teacher_user.profile.role = "Teacher"
    teacher_user.profile.save()

    # Authenticate as the teacher
    client.login(username="teacher", password="test123")

    # Test course enrollment endpoint
    response = client.post("/api/courses/enroll/", {"student_id": 1, "course_id": 1})
    assert response.status_code == 200
    assert response.data["status"] == "Enrollment successful"
