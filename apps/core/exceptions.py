"""
Learnova LMS - Custom Exception Handlers
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def learnova_exception_handler(exc, context):
    """
    Custom exception handler for consistent API error responses.
    Returns: { "success": false, "error": "...", "details": {...} }
    """
    response = exception_handler(exc, context)
    if response is not None:
        custom_response = {
            "success": False,
            "error": str(exc) if hasattr(exc, 'args') and exc.args else "An error occurred",
            "status_code": response.status_code,
        }
        if hasattr(exc, 'detail'):
            custom_response["details"] = exc.detail
        response.data = custom_response
    return response


class LearnovaValidationError(Exception):
    """Base validation error for business logic."""

    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class EnrollmentClosedError(LearnovaValidationError):
    """Raised when enrollment is closed for a course."""

    pass


class DuplicateEnrollmentError(LearnovaValidationError):
    """Raised when user is already enrolled."""

    pass


class QuizAttemptLimitError(LearnovaValidationError):
    """Raised when quiz attempt limit exceeded."""

    pass


class CourseNotPublishedError(LearnovaValidationError):
    """Raised when accessing unpublished course."""

    pass
