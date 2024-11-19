from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet
from .models import User
from .serializers import UserSerializer, CustomUserCreateSerializer

class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    # Use CustomUserCreateSerializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get("role")
        if role in ['Student', 'Teacher', 'Admin']:
            user.role = role
            user.save()
            return Response({"message": f"Role '{role}' assigned to {user.username}"})
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
