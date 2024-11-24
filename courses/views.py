from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from users.views import logger
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsTeacher, IsAdmin
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import action





class CoursePagination(PageNumberPagination):
    page_size = 10  # Number of courses per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum number of items per page



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['name', 'instructor']  # Filters by name and instructor
    search_fields = ['name', 'description']  # Search by name or description
    ordering_fields = ['name', 'instructor']  # Ordering options
    ordering = ['name']  # Default ordering

    @action(detail=False, methods=['get'])
    def cached_courses(self, request):
        user = request.user
        cache_key = f"courses_{user.id}_{user.role}"
        courses = cache.get(cache_key)

        if courses:
            logger.info(f"Cache hit: {cache_key}")
        else:
            logger.info(f"Cache miss: {cache_key}")
            courses = Course.objects.all()  # Replace with appropriate query
            serialized_data = CourseSerializer(courses, many=True).data
            cache.set(cache_key, serialized_data, timeout=3600)

        return Response(courses)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher | IsAdmin]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        user = request.user
        cache_key = f"courses_{user.id}_{user.role}"
        cache.delete(cache_key)  # Clear cached courses
        return response


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        enrollment = Enrollment.objects.create(
            student=request.data['student'],
            course=request.data['course']
        )
        logger.info(f"Course enrollment: Student {enrollment.student.id} enrolled in Course {enrollment.course.id}")
        return Response({"status": "Enrollment successful"})
