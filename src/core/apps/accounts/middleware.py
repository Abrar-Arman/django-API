from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class AdminRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        if request.path.startswith("/api/v1/users/") and request.path.endswith("/set-role/"):
            try:
                user, token = self.jwt_auth.authenticate(request)
                if user is None:
                    return JsonResponse(
                        {"detail": "Authentication required"},
                        status=401
                    )

                if user.role != "admin":
                    return JsonResponse(
                        {"detail": "Admin role required"},
                        status=403
                    )

                request.user = user

            except AuthenticationFailed as e:
                return JsonResponse(
                    {"detail": str(e)},
                    status=401
                )

        response = self.get_response(request)
        return response

