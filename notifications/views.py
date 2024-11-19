from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class ManageNotificationsView(ViewSet):
    def list(self, request):
        # Example implementation
        return Response({"message": "List of notifications"})

    def create(self, request):
        # Example implementation
        return Response({"message": "Notification created"})
