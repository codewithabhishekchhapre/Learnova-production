from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment, LessonProgress, Certificate
from .serializers import EnrollmentSerializer, LessonProgressSerializer, CertificateSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Enrollment.objects.filter(student=user)
        if user.is_instructor:
            return Enrollment.objects.filter(course__instructor=user)
        return Enrollment.objects.all()

    @action(detail=False, methods=['post'], url_path='enroll')
    def enroll(self, request):
        """Student enrolls in a course. POST { "course_id": 1 }"""
        from apps.courses.models import Course
        course_id = request.data.get('course_id')
        if not course_id:
            return Response(
                {'error': 'course_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.user.is_student:
            return Response(
                {'error': 'Only students can enroll'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            course = Course.objects.get(pk=course_id, status=Course.Status.PUBLISHED)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found or not published'},
                status=status.HTTP_404_NOT_FOUND
            )
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {'error': 'Already enrolled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='my-courses')
    def my_courses(self, request):
        """Student dashboard - my enrolled courses with progress."""
        if not request.user.is_student:
            return Response({'error': 'Students only'}, status=status.HTTP_403_FORBIDDEN)
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
        return Response(EnrollmentSerializer(enrollments, many=True).data)


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return LessonProgress.objects.filter(enrollment__student=user)
        return LessonProgress.objects.all()


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """Certificates - Student sees their own, Instructor/Admin see all."""
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return Certificate.objects.filter(enrollment__student=user)
        if user.is_instructor:
            return Certificate.objects.filter(enrollment__course__instructor=user)
        return Certificate.objects.all()
