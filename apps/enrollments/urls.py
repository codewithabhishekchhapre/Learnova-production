from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, LessonProgressViewSet, CertificateViewSet

router = DefaultRouter()
router.register('', EnrollmentViewSet, basename='enrollment')
router.register('lesson-progress', LessonProgressViewSet, basename='lesson-progress')
router.register('certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
]
