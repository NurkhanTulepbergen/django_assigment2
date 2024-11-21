from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from attendance.models import Attendance
from grades.models import Grade
from students.models import Student

@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please mark your attendance for today.",
            from_email="noreply@studentmanagementsystem.com",
            recipient_list=[student.email],
        )
    return f"Attendance reminders sent to {len(students)} students."

@shared_task
def send_grade_update_notification(student_id, course_name, grade):
    student = Student.objects.get(id=student_id)
    send_mail(
        subject="Grade Update Notification",
        message=f"Your grade for the course {course_name} has been updated to {grade}.",
        from_email="noreply@studentmanagementsystem.com",
        recipient_list=[student.email],
    )
    return f"Grade update notification sent to {student.email}."

@shared_task
def send_daily_report():
    # Generate and send daily summary of attendance and grades
    summary = "Daily Report:\n\n"
    for student in Student.objects.all():
        summary += f"{student.name}: {student.attendance_set.count()} attendance entries\n"
        summary += f"{student.grade_set.count()} grades\n\n"
    send_mail(
        subject="Daily Attendance and Grade Report",
        message=summary,
        from_email="noreply@studentmanagementsystem.com",
        recipient_list=["admin@studentmanagementsystem.com"],
    )
    return "Daily report sent."

@shared_task
def send_weekly_performance_summary():
    # Generate and send weekly performance summary
    summary = "Weekly Performance Summary:\n\n"
    for student in Student.objects.all():
        summary += f"{student.name}:\n"
        summary += f"Courses Enrolled: {student.enrollments.count()}\n"
        summary += f"Grades: {', '.join([str(grade.grade) for grade in student.grade_set.all()])}\n\n"
    send_mail(
        subject="Weekly Performance Summary",
        message=summary,
        from_email="noreply@studentmanagementsystem.com",
        recipient_list=["admin@studentmanagementsystem.com"],
    )
    return "Weekly summary sent."

