from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.communications.views import AnnouncementViewSet

router = DefaultRouter()
router.register('announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
