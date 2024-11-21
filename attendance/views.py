from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.views import logger
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher, IsAdmin

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher | IsAdmin]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        attendance = self.get_object()
        logger.info(
            f"Attendance marked: Student {attendance.student.id} in Course {attendance.course.id} - Status: {attendance.status}")
        return response
