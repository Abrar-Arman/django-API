from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..models import CustomUser

from ..serializers import (MyTokenObtainPairSerializer,
                          RegisterSerializer, SetRoleSerializer,
                          )


@extend_schema(tags=["Accounts"])
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


@extend_schema(tags=["Accounts"])
class SetRoleView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SetRoleSerializer
    lookup_field = "id"


@extend_schema(tags=["Accounts"])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(
    description="Refresh access token using refresh token",
    tags=["Accounts"]
)
class MyTokenRefreshView(TokenRefreshView):
    pass