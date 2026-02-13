from rest_framework import   viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminOrReadOnly

from ..models import Category
from ..serializers import (CategoryDetailSerializer, CategoryListSerializer
                          )


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