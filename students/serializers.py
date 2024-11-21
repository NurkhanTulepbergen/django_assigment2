from rest_framework import serializers
from .models import Student
from courses.serializers import CourseSerializer
from grades.serializers import GradeSerializer
from attendance.serializers import AttendanceSerializer

class StudentSerializer(serializers.ModelSerializer):
    enrollments = CourseSerializer(many=True, source='enrollments.course', read_only=True)
    grades = GradeSerializer(many=True, read_only=True)
    attendance = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'dob', 'registration_date', 'enrollments', 'grades', 'attendance']
