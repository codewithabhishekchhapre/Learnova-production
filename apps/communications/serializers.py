"""
Communications serializers for Learnova LMS
"""
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Announcement


class AnnouncementSerializer(BaseModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'course', 'author', 'author_name', 'title', 'content', 'scope', 'is_pinned', 'created_at', 'updated_at']
