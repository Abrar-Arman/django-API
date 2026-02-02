from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema,OpenApiParameter

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsEnrolledStudent,IsReviewOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsEnrolledStudent,IsReviewOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        course_id = self.request.query_params.get('course')

        if course_id:
            return self.queryset.filter(course_id=course_id)
        return self.queryset
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='course',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter reviews by course ID'
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
       

