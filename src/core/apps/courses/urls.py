from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CourseViewSet, EnrollViewSet,
                    LessonCompleteAPIView, LessonViewSet,
                    UserLessonProgressListAPIView)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"enrollments", EnrollViewSet, basename="enroll")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "lessons-progress/",
        UserLessonProgressListAPIView.as_view(),
        name="user-progress",
    ),
    path(
        "lessons/<int:lesson_id>/complete/",
        LessonCompleteAPIView.as_view(),
        name="lesson-complete",
    ),
]
