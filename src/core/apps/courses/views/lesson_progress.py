from rest_framework import ( generics, serializers, status,
                           )
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response


from ..models import Lesson, LessonProgress
from ..serializers import (LessonProgressListSerializer,
                          LessonProgressSerializer)

@extend_schema(tags=["Progress"])
class UserLessonProgressListAPIView(generics.ListAPIView):
    serializer_class = LessonProgressListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(
            user=self.request.user
        ).select_related("lesson", "lesson__course")


@extend_schema(tags=["Progress"])
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
