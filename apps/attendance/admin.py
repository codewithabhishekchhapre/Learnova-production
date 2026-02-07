from django.contrib import admin
from .models import LiveSession, Attendance


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'session_date', 'duration_minutes']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['session', 'student', 'status']
