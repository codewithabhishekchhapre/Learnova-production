from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LiveSession, Attendance
from .serializers import LiveSessionSerializer, AttendanceSerializer


class LiveSessionViewSet(viewsets.ModelViewSet):
    serializer_class = LiveSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = LiveSession.objects.select_related('course')
        if getattr(self.request.user, 'is_instructor', False):
            return qs.filter(course__instructor=self.request.user)
        if getattr(self.request.user, 'is_student', False):
            return qs.filter(course__enrollments__student=self.request.user).distinct()
        return qs


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
