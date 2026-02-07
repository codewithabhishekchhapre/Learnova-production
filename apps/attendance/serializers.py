"""
Attendance serializers for Learnova LMS
"""
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import LiveSession, Attendance


class LiveSessionSerializer(BaseModelSerializer):
    class Meta:
        model = LiveSession
        fields = ['id', 'course', 'title', 'session_date', 'duration_minutes', 'meeting_url', 'created_at', 'updated_at']


class AttendanceSerializer(BaseModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'session', 'student', 'status', 'notes']
