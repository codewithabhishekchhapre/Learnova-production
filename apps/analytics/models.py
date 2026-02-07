"""
Analytics models for Learnova LMS
Reports, dashboards
"""
from django.db import models


class Report(models.Model):
    """Stored report configuration/snapshot."""

    class ReportType(models.TextChoices):
        ENROLLMENT = 'ENROLLMENT', 'Enrollment Report'
        COMPLETION = 'COMPLETION', 'Completion Rate'
        REVENUE = 'REVENUE', 'Revenue Report'
        PERFORMANCE = 'PERFORMANCE', 'Student Performance'

    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    title = models.CharField(max_length=255)
    params = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
