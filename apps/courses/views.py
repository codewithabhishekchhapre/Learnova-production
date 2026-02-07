from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.permissions import IsInstructorOrAdmin, CanEditCourse, IsAdminUser
from .models import Category, Course, Module, Lesson
from .serializers import CategorySerializer, CourseSerializer, CourseListSerializer, ModuleSerializer, LessonSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category', 'instructor', 'audience']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated(), IsInstructorOrAdmin(), CanEditCourse()]

    def get_queryset(self):
        qs = Course.objects.all()
        # Unauthenticated users and students see only published courses
        if not self.request.user.is_authenticated:
            return qs.filter(status=Course.Status.PUBLISHED)
        if hasattr(self.request.user, 'is_student') and self.request.user.is_student:
            return qs.filter(status=Course.Status.PUBLISHED)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        if self.request.user.role == 'INSTRUCTOR':
            serializer.save(instructor=self.request.user)
        else:
            # Admin: use selected instructor or self if none provided
            instructor = serializer.validated_data.get('instructor') or self.request.user
            serializer.save(instructor=instructor)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
