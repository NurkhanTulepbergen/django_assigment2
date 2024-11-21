from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.views import logger
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsTeacher, IsAdmin
from notifications.tasks import send_grade_update_notification


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher | IsAdmin]
        return super().get_permissions()



    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        grade = self.get_object()
        logger.info(
            f"Grade updated: Student {grade.student.id} in Course {grade.course.id} - New Grade: {grade.grade}")
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        grade = self.get_object()
        send_grade_update_notification.delay(
            student_id=grade.student.id,
            course_name=grade.course.name,
            grade=grade.grade,
        )
        return response