"""
Learnova LMS - Common Permission Classes
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Only admin users can access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class IsInstructorOrAdmin(permissions.BasePermission):
    """Instructor or Admin can access."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('INSTRUCTOR', 'ADMIN')
        )


class IsStudent(permissions.BasePermission):
    """Only students can access."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'


class IsCourseInstructor(permissions.BasePermission):
    """User must be the instructor of the course."""

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'instructor') and obj.instructor == request.user


class CanEditCourse(permissions.BasePermission):
    """Admin can edit any course; Instructor can edit only their own."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        return hasattr(obj, 'instructor') and obj.instructor == request.user


class IsEnrolledStudent(permissions.BasePermission):
    """User must be enrolled in the course."""

    def has_object_permission(self, request, view, obj):
        course = getattr(obj, 'course', obj) if hasattr(obj, 'course') else obj
        return request.user.enrollments.filter(course=course).exists()


class ReadOnly(permissions.BasePermission):
    """Allow only read operations."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
