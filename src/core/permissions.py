from rest_framework.permissions import SAFE_METHODS, BasePermission
from core.apps.courses.models import Course
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "admin"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "instructor"


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.created_by.id == request.user.id


class IsLessonCourseOwner(BasePermission):
     def has_permission(self, request, view):
        if request.method == "POST":
            course_id = request.data.get("course_id")
            if not course_id:
                return False
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return False
            return course.created_by == request.user
        return True
     
     def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.course.created_by == request.user


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True

        return obj == request.user
