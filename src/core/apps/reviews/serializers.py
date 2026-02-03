from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "course",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value

    def validate(self, attrs):

        request = self.context.get("request")
        user = request.user
        course = attrs.get("course")

        if Review.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError(
                "You have already reviewed this course."
            )

        return attrs

    def create(self, validated_data):

        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
