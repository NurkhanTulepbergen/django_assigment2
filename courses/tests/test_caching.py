from django.core.cache import cache
import pytest
from rest_framework.test import APIClient
import django
from django.conf import settings

# Ensure that Django settings are configured before any tests
settings.configure(default_settings='StudentManagementSystem.settings')
django.setup()

@pytest.mark.django_db
def test_course_caching():
    client = APIClient()

    # Fetch courses for the first time
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert "Math 101" in response.data["results"]

    # Simulate caching
    cache.set("courses_list", response.data, timeout=3600)

    # Fetch courses from cache
    cached_data = cache.get("courses_list")
    assert cached_data is not None
    assert "Math 101" in cached_data["results"]
