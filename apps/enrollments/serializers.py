"""
Enrollment serializers for Learnova LMS
"""
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Enrollment, LessonProgress, Certificate


class LessonProgressSerializer(BaseModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'completed', 'completed_at']


class EnrollmentSerializer(BaseModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'student_email', 'course', 'course_title', 'status', 'progress_percent', 'enrolled_at', 'completed_at']


class CertificateSerializer(BaseModelSerializer):
    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'certificate_id', 'enrollment', 'course_title', 'student_name', 'issued_at']
