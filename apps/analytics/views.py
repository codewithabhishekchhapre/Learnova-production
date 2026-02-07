from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DashboardViewSet(viewsets.ViewSet):
    """Analytics dashboard endpoints."""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Admin dashboard overview metrics."""
        from apps.courses.models import Course
        from apps.enrollments.models import Enrollment
        from apps.users.models import User

        from apps.courses.models import Category
        return Response({
            'total_courses': Course.objects.count(),
            'total_students': User.objects.filter(role='STUDENT').count(),
            'total_instructors': User.objects.filter(role='INSTRUCTOR').count(),
            'total_enrollments': Enrollment.objects.count(),
            'total_categories': Category.objects.count(),
        })

    @action(detail=False, methods=['get'], url_path='instructor/students')
    def instructor_students(self, request):
        """Instructor: Students in my courses. ?course_id=1 to filter by course."""
        from apps.enrollments.models import Enrollment
        from apps.users.serializers import UserSerializer

        if not request.user.is_instructor:
            return Response({'error': 'Instructors only'}, status=403)
        qs = Enrollment.objects.filter(
            course__instructor=request.user
        ).select_related('student', 'course')
        course_id = request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)
        data = [
            {
                'student': UserSerializer(e.student).data,
                'course_id': e.course_id,
                'course_title': e.course.title,
                'progress_percent': float(e.progress_percent),
                'status': e.status,
                'enrolled_at': e.enrolled_at,
            }
            for e in qs
        ]
        return Response(data)
