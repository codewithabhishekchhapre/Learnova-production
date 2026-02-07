from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizAttemptViewSet, AssignmentViewSet, AssignmentSubmissionViewSet

router = DefaultRouter()
router.register('quizzes', QuizViewSet, basename='quiz')
router.register('quiz-attempts', QuizAttemptViewSet, basename='quiz-attempt')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('submissions', AssignmentSubmissionViewSet, basename='assignment-submission')

urlpatterns = [
    path('', include(router.urls)),
]
