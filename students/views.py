from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent
from django.core.cache import cache
from rest_framework.response import Response


class StudentPagination(PageNumberPagination):
    page_size = 10  # Number of students per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum number of items per page

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    #pagination_class = StudentPagination  # Enable pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['name', 'email', 'dob']  # Filters by name, email, and dob
    search_fields = ['name', 'email']  # Search by name or email
    ordering_fields = ['name', 'dob']  # Ordering options
    ordering = ['name']  # Default ordering

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        student_id = kwargs.get('pk')
        cache_key = f"student_{student_id}"
        cache.delete(cache_key)  # Clear cached student data
        return response

    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        cache_key = f"student_{student_id}"
        student_data = cache.get(cache_key)

        if not student_data:
            student = self.get_object()
            student_data = StudentSerializer(student).data
            cache.set(cache_key, student_data, timeout=3600)  # Cache for 1 hour
        return Response(student_data)


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
