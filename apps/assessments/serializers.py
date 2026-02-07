"""
Assessment serializers for Learnova LMS
"""
from rest_framework import serializers
from apps.core.serializers import BaseModelSerializer
from .models import Quiz, Question, QuestionOption, QuizAttempt, Assignment, AssignmentSubmission


class QuestionOptionSerializer(BaseModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'option_text', 'is_correct', 'order']


class QuestionSerializer(BaseModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'options']


class QuizSerializer(BaseModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'time_limit_minutes', 'passing_score', 'max_attempts', 'is_published', 'questions', 'created_at', 'updated_at']


class QuizAttemptSerializer(BaseModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'student', 'quiz', 'score', 'passed', 'started_at', 'submitted_at']


class AssignmentSerializer(BaseModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date', 'max_points', 'created_at', 'updated_at']


class AssignmentSubmissionSerializer(BaseModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'file', 'text_submission', 'grade', 'feedback', 'submitted_at', 'graded_at']
