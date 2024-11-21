import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import django
from django.conf import settings

# Ensure that Django settings are configured before any tests
settings.configure(default_settings='StudentManagementSystem.settings')
django.setup()
@pytest.mark.django_db
def test_role_based_access():
    client = APIClient()

    # Create admin, teacher, and student users
    admin = User.objects.create_superuser(username="admin", password="admin123")
    teacher = User.objects.create_user(username="teacher", password="teacher123")
    student = User.objects.create_user(username="student", password="student123")

    # Admin should access everything
    client.login(username="admin", password="admin123")
    response = client.get("/api/students/")
    assert response.status_code == 200

    # Teacher should access teacher-specific data
    client.login(username="teacher", password="teacher123")
    response = client.get("/api/students/")
    assert response.status_code == 403

    # Student should access only their data
    client.login(username="student", password="student123")
    response = client.get("/api/students/1/")
    assert response.status_code == 200
