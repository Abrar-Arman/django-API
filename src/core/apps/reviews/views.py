from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .permissions import IsEnrolledStudent, IsReviewOwnerOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsEnrolledStudent,
        IsReviewOwnerOrReadOnly,
    ]

    def get_queryset(self):
        course_id = self.request.query_params.get("course")

        if course_id:
            return self.queryset.filter(course_id=course_id)
        return self.queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="course",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter reviews by course ID",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
