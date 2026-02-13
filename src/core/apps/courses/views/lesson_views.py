from rest_framework import ( mixins,
                            viewsets)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from core.permissions import (IsInstructor,
                              IsLessonCourseOwner)

from ..models import  Lesson
from ..serializers import  LessonSerializer

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