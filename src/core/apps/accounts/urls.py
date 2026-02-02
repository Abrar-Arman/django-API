from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, SetRoleView,MyTokenObtainPairView, UserProfileViewSet

router=DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<int:id>/set-role/', SetRoleView.as_view(), name='set_role'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('', include(router.urls))

]
