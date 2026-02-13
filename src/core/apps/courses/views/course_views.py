from rest_framework import (filters,
                            viewsets)

from rest_framework.permissions import IsAuthenticated

from core.permissions import ( IsCourseOwner, IsInstructor
                              )

from ..models import  Course
from ..serializers import (
                          CourseDetailSerializer, CourseSerializer
                         )


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related("lessons").all()
    permission_classes = [IsAuthenticated, IsInstructor, IsCourseOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer
