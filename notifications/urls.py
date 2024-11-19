from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManageNotificationsView

router = DefaultRouter()
router.register(r'', ManageNotificationsView, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]
