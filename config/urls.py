"""
Learnova LMS - Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/courses/', include('apps.courses.urls')),
    path('api/v1/enrollments/', include('apps.enrollments.urls')),
    path('api/v1/assessments/', include('apps.assessments.urls')),
    path('api/v1/attendance/', include('apps.attendance.urls')),
    path('api/v1/communications/', include('apps.communications.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
