"""
Attendance models for Learnova LMS
"""
from django.db import models
from django.conf import settings


class LiveSession(models.Model):
    """Scheduled live session for a course."""

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='live_sessions')
    title = models.CharField(max_length=255)
    session_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    meeting_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'live_sessions'


class Attendance(models.Model):
    """Student attendance record for a live session."""

    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'
        EXCUSED = 'EXCUSED', 'Excused'

    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=Status.choices)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'attendance'
        unique_together = ['session', 'student']
