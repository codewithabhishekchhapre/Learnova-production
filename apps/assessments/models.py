"""
Assessment models for Learnova LMS
Quizzes, Exams, Assignments
"""
from django.db import models
from django.conf import settings
from apps.core.validators import validate_percentage, validate_quiz_time_limit


class Quiz(models.Model):
    """Quiz/Exam for a course."""

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(null=True, blank=True, validators=[validate_quiz_time_limit])
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=60, validators=[validate_percentage])
    max_attempts = models.PositiveIntegerField(default=3)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quizzes'

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    """Question within a quiz."""

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MULTIPLE_CHOICE', 'Multiple Choice'
        TRUE_FALSE = 'TRUE_FALSE', 'True/False'
        SHORT_ANSWER = 'SHORT_ANSWER', 'Short Answer'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'quiz_questions'
        ordering = ['order']


class QuestionOption(models.Model):
    """Options for multiple choice/true-false questions."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'question_options'
        ordering = ['order']


class QuizAttempt(models.Model):
    """Student quiz attempt."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'quiz_attempts'
        ordering = ['-started_at']


class Assignment(models.Model):
    """Assignment for a course."""

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    max_points = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class AssignmentSubmission(models.Model):
    """Student assignment submission."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    text_submission = models.TextField(blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'assignment_submissions'
        unique_together = ['assignment', 'student']
