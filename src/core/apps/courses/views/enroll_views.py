from rest_framework import ( mixins, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import  Enroll
from ..serializers import EnrollSerializer




class EnrollViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = EnrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if  user.role == "student":
            return Enroll.objects.filter(user=user)
        return Enroll.objects.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="pending")

    def destroy(self, request, *args, **kwargs):
        enrollment = self.get_object()
        if enrollment.status != "pending":
            return Response(
                {
                    "detail": "Cannot remove enrollment that is already confirmed."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True, methods=["patch"], permission_classes=[IsAuthenticated]
    )
    def set_status(self, request, pk=None):

        enrollment = self.get_object()
        course = enrollment.course

        if request.user != course.created_by:
            return Response(
                {"detail": "Only the instructor can set enrollment status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        status_value = request.data.get("status")
        if status_value not in ["confirmed", "rejected"]:
            return Response(
                {
                    "detail": "Invalid status. Must be 'confirmed' or 'rejected'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        enrollment.status = status_value
        enrollment.save()
        return Response(self.get_serializer(enrollment).data)