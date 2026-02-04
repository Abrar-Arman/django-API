from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (MyTokenObtainPairView, RegisterView, SetRoleView,
                    UserProfileViewSet, MyTokenRefreshView,UserViewSet )

router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet, basename="profile")
router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/<int:id>/set-role/", SetRoleView.as_view(), name="set_role"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),  
    path("", include(router.urls)),
]
