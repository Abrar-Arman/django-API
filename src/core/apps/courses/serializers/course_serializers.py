from rest_framework import serializers

from ..models import Category, Course
from .lesson_serializers import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    id = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "level",
            "category_id",
            "created_by",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        return super().create(validated_data)


class CourseDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "level",
            "created_by",
            "lessons",
        ]

    def get_lessons(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated and obj.created_by == user:
            return LessonSerializer(
                obj.lessons.all(), many=True, context=self.context
            ).data

        if user and user.is_authenticated:
            if obj.registrations.filter(
                user=user, status="confirmed"
            ).exists():
                return LessonSerializer(
                    obj.lessons.all(), many=True, context=self.context
                ).data

        first_lesson = obj.lessons.order_by("order").first()
        if first_lesson:
            return [LessonSerializer(first_lesson, context=self.context).data]

        return []