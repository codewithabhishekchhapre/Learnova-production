from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question, QuizAttempt, Assignment, AssignmentSubmission
from .serializers import QuizSerializer, QuizAttemptSerializer, AssignmentSerializer, AssignmentSubmissionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Assignment.objects.select_related('course')
        if getattr(self.request.user, 'is_instructor', False):
            return qs.filter(course__instructor=self.request.user)
        if getattr(self.request.user, 'is_student', False):
            return qs.filter(course__enrollments__student=self.request.user).distinct()
        return qs


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated]
