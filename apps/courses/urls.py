from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, ModuleViewSet, LessonViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('', CourseViewSet, basename='course')
router.register('modules', ModuleViewSet, basename='module')
router.register('lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
]
