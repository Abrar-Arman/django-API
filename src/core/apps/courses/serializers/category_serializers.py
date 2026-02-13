from rest_framework import serializers

from ..models import Category
from .course_serializers import CourseSerializer

class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    courses = CourseSerializer(source="course_set", many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "courses"]
