from rest_framework import serializers

from ..models import Course, Enroll

class EnrollSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
    )

    class Meta:
        model = Enroll
        fields = [
            "id",
            "user",
            "course",
            "course_id",
            "status",
            "registered_at",
        ]
        read_only_fields = ["id", "user", "course", "status", "registered_at"]
