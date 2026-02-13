from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from ..models import UserProfile

from ..serializers import ( ProfileImageSerializer,
                          UserProfileSerializer)


@extend_schema(tags=["Profile"])
@extend_schema_view(
    create=extend_schema(
        description="Creating profiles is **not allowed**",
        responses={405: "Method not allowed"},
    ),
    list=extend_schema(
        description="Listing profiles is **not allowed**",
        responses={405: "Method not allowed"},
    ),
    retrieve=extend_schema(
        description="Retrieving a profile is **not allowed**",
        responses={405: "Method not allowed"},
    ),
    destroy=extend_schema(
        description="Deleting profiles is **not allowed**",
        responses={405: "Method not allowed"},
    ),
    update=extend_schema(description="Update only your own profile"),
    partial_update=extend_schema(
        description="Partial update only your own profile"
    ),
    upload_image=extend_schema(
        description="Upload profile image (PATCH method)"
    ),
)
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ProfileImageSerializer
        return UserProfileSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method 'POST' not allowed."}, status=405)

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Method 'Get' not allowed."}, status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response({"detail": "Method 'GET' not allowed."}, status=405)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return Response(
                {"detail": "You cannot update another user's profile."},
                status=403,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return Response(
                {"detail": "You cannot update another user's profile."},
                status=403,
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method 'GET' not allowed."}, status=405)

    @action(
        detail=True, methods=["patch"], serializer_class=ProfileImageSerializer
    )
    def upload_image(self, request, pk=None):
        profile = self.get_object()
        if profile.user != request.user:
            return Response(
                {"detail": "You cannot upload image for another user."},
                status=403,
            )
        serializer = self.get_serializer(
            profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



       