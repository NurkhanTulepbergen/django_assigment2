from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsTeacher

class TeacherOnlyView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response({"message": "Hello, Teacher!"})
