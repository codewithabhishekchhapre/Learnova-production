from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.communications.models import Announcement
from apps.communications.serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Announcement.objects.select_related('course', 'author')
        if getattr(self.request.user, 'is_instructor', False):
            return qs.filter(course__instructor=self.request.user)
        if getattr(self.request.user, 'is_student', False):
            from apps.enrollments.models import Enrollment
            enrolled = Enrollment.objects.filter(student=self.request.user).values_list('course_id', flat=True)
            return qs.filter(Q(course_id__in=enrolled) | Q(scope='SYSTEM'))
        return qs
