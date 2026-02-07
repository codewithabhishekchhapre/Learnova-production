from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, DashboardViewSet

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')
router.register('dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
