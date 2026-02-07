"""
Course models for Learnova LMS
"""
from django.db import models
from django.conf import settings
from apps.core.validators import validate_slug_format


class Category(models.Model):
    """Course category for organization."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, validators=[validate_slug_format])
    description = models.TextField(blank=True)
    class_range = models.CharField(max_length=50, blank=True, help_text="e.g. Class LKG - 8, Class 3 - 13")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    """Main course model."""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending Approval'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    class Audience(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        KIDS = 'KIDS', 'Kids'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, validators=[validate_slug_format])
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    audience = models.CharField(max_length=20, choices=Audience.choices, default=Audience.STUDENT)
    class_range = models.CharField(max_length=50, blank=True, help_text="e.g. LKG - 8, Class 3 - 12")
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    duration_hours = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=50, default='Beginner')
    max_students = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Course module/section."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_modules'
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """Lesson/content within a module."""

    class ContentType(models.TextChoices):
        VIDEO = 'VIDEO', 'Video'
        PDF = 'PDF', 'PDF'
        TEXT = 'TEXT', 'Text'
        LINK = 'LINK', 'External Link'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    content_url = models.URLField(blank=True)
    content_file = models.FileField(upload_to='lessons/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_lessons'
        ordering = ['order']

