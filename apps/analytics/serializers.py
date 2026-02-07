"""
Analytics serializers for Learnova LMS
"""
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Report


class ReportSerializer(BaseModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'title', 'params', 'generated_at']
