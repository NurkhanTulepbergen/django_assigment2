from django.db import models
from students.models import Student
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()  # Teachers are part of the user system

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2)  # e.g., A, B+, C
    date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_grades')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.grade}"
