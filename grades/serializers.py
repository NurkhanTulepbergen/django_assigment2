from rest_framework import serializers
from grades.models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student_name', 'course_name', 'grade', 'date', 'teacher']
