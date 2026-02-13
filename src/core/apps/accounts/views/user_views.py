from drf_spectacular.utils import extend_schema
from rest_framework import  viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CustomUser
from core.permissions import IsAdminOrReadOnly,IsAdmin,IsAdminOrOwner

from ..serializers import UserSerializer


@extend_schema(tags=["Users"])    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated,IsAdmin]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated,IsAdminOrOwner]
        return [perm() for perm in permission_classes]
       