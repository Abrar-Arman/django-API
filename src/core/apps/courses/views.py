from rest_framework import (filters, generics, mixins, serializers, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import (IsAdminOrReadOnly, IsCourseOwner, IsInstructor,
                              IsLessonCourseOwner)

from .models import Category, Course, Enroll, Lesson, LessonProgress
from .serializers import (CategoryDetailSerializer, CategoryListSerializer,
                          CourseDetailSerializer, CourseSerializer,
                          EnrollSerializer, LessonProgressListSerializer,
                          LessonProgressSerializer, LessonSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("course_set").all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "retrieve":
            return CategoryDetailSerializer
        if self.action == "create":
            return CategoryListSerializer
        return CategoryListSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related("lessons").all()
    permission_classes = [IsAuthenticated, IsInstructor, IsCourseOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsLessonCourseOwner]
    parser_classes = [MultiPartParser, FormParser]


class EnrollViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = EnrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            user = self.request.user
            if user.role == "student":
                return Enroll.objects.filter(user=user)
            elif user.role == "instructor":
                return Enroll.objects.filter(course__created_by=user)
            else:
                return Enroll.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")

    def destroy(self, request, *args, **kwargs):
        enrollment = self.get_object()
        if enrollment.status != "pending":
            return Response(
                {
                    "detail": "Cannot remove enrollment that is already confirmed."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True, methods=["patch"], permission_classes=[IsAuthenticated]
    )
    def set_status(self, request, pk=None):

        enrollment = self.get_object()
        course = enrollment.course

        if request.user != course.created_by:
            return Response(
                {"detail": "Only the instructor can set enrollment status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        status_value = request.data.get("status")
        if status_value not in ["confirmed", "rejected"]:
            return Response(
                {
                    "detail": "Invalid status. Must be 'confirmed' or 'rejected'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        enrollment.status = status_value
        enrollment.save()
        return Response(self.get_serializer(enrollment).data)


class UserLessonProgressListAPIView(generics.ListAPIView):
    serializer_class = LessonProgressListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(
            user=self.request.user
        ).select_related("lesson", "lesson__course")


class LessonCompleteAPIView(generics.CreateAPIView):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lesson_id = self.kwargs["lesson_id"]
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            raise serializers.ValidationError({"lesson": "Lesson not found."})
        context["lesson"] = lesson
        context["user"] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        if result.get("action") == "marked":
            return Response(
                {"detail": "Lesson marked as completed."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Lesson unmarked (completion removed)."},
                status=status.HTTP_200_OK,
            )
