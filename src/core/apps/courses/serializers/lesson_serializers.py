from rest_framework import serializers

from ..models import  Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "order",
            "video_file",
            "document_file",
            "course_id",
        ]

    def validate_video_file(self, value):
        if value:
            if not value.name.lower().endswith((".mp4", ".mov", ".avi")):
                raise serializers.ValidationError(
                    "Video must be MP4, MOV, or AVI."
                )
        return value

    def validate_document_file(self, value):
        if value:
            if not value.name.lower().endswith((".pdf", ".docx")):
                raise serializers.ValidationError(
                    "Document must be PDF or DOCX."
                )
        return value
