from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsAdminOrInstructor

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,IsAdminOrInstructor]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Notification.objects.all().order_by("-created_at")
        elif user.role == "instructor":
            return Notification.objects.filter(recipient=user).order_by("-created_at")
