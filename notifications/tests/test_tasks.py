from notifications.tasks import send_daily_attendance_reminder, send_grade_update_notification
import pytest
import django
from django.conf import settings

# Ensure that Django settings are configured before any tests
settings.configure(default_settings='StudentManagementSystem.settings')
django.setup()
@pytest.mark.django_db
def test_send_daily_attendance_reminder(mailoutbox):
    # Call the task
    send_daily_attendance_reminder()

    # Check if email was sent
    assert len(mailoutbox) > 0
    assert "Daily Attendance Reminder" in mailoutbox[0].subject

@pytest.mark.django_db
def test_send_grade_update_notification(mailoutbox):
    # Simulate a grade update
    send_grade_update_notification(student_id=1, course_name="Math 101", grade="A")

    # Check if email was sent
    assert len(mailoutbox) == 1
    assert "Grade Update Notification" in mailoutbox[0].subject
    assert "Math 101" in mailoutbox[0].body
