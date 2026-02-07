"""
Enrollment models for Learnova LMS
"""
from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    """Student course enrollment."""

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        DROPPED = 'DROPPED', 'Dropped'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"


class LessonProgress(models.Model):
    """Track lesson completion per student."""

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['enrollment', 'lesson']


class Certificate(models.Model):
    """Certificate issued on course completion."""

    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=50, unique=True, editable=False)

    class Meta:
        db_table = 'certificates'

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            self.certificate_id = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
