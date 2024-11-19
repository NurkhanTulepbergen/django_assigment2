from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsStudent]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.role == 'Student':
            return self.queryset.filter(user=self.request.user)
        return self.queryset
