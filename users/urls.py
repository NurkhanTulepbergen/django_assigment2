from django.urls import path
from .views import TeacherOnlyView

urlpatterns = [
    path('teacher-only/', TeacherOnlyView.as_view(), name='teacher-only'),
]