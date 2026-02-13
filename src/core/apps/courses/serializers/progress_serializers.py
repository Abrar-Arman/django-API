from rest_framework import serializers

from ..models import LessonProgress

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = []

    def create(self, validated_data):
        user = self.context["user"]
        lesson = self.context["lesson"]

        progress, created = LessonProgress.objects.get_or_create(
            user=user, lesson=lesson
        )
        if not created:
            progress.delete()
            return {"action": "unmarked"}
        return {"action": "marked"}


class LessonProgressListSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    course_title = serializers.CharField(
        source="lesson.course.title", read_only=True
    )
    completed_at = serializers.DateTimeField(read_only=True)
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson_title",
            "course_title",
            "completed_at",
            "completion_percentage",
        ]

    def get_completion_percentage(self, obj):

        course = obj.lesson.course
        user = obj.user

        total_lessons = course.lessons.count()
        if total_lessons == 0:
            return 0

        completed_lessons = LessonProgress.objects.filter(
            user=user, lesson__course=course
        ).count()

        return round((completed_lessons / total_lessons) * 100, 2)