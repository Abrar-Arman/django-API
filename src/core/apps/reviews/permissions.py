from rest_framework.permissions import SAFE_METHODS, BasePermission

from core.apps.courses.models import Enroll


class IsEnrolledStudent(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            course_id = request.data.get("course")
            if not course_id:
                return False
            return Enroll.objects.filter(
                user=request.user, course_id=course_id
            ).exists()
        return True


class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
