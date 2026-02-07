"""
Communications models for Learnova LMS
Announcements
"""
from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """Course or system-wide announcement."""

    class Scope(models.TextChoices):
        COURSE = 'COURSE', 'Course'
        SYSTEM = 'SYSTEM', 'System-wide'

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    content = models.TextField()
    scope = models.CharField(max_length=20, choices=Scope.choices, default=Scope.COURSE)
    is_pinned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
