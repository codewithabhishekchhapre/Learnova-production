"""
Course serializers for Learnova LMS
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Category, Course, Module, Lesson

User = get_user_model()


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'class_range', 'parent', 'created_at', 'updated_at']


class LessonSerializer(BaseModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content_type', 'content_url', 'duration_minutes', 'order', 'created_at', 'updated_at']


class ModuleSerializer(BaseModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons', 'created_at', 'updated_at']


class CourseSerializer(BaseModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'category', 'category_name',
            'instructor', 'instructor_name', 'status', 'audience', 'class_range',
            'thumbnail', 'duration_hours', 'level', 'max_students',
            'modules', 'created_at', 'updated_at'
        ]



class CourseListSerializer(BaseModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'category_name', 'instructor_name', 'status', 'audience', 'class_range', 'thumbnail', 'duration_hours', 'level']
