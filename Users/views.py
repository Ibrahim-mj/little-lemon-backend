from django.contrib.auth import authenticate, login
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserCreateSerializer, CustomTokenObtainPairSerializer


class UserViewSet(UserViewSet):
    """
    A viewset for handling user creation.

    Methods:
    - get_queryset: Retrieves the queryset of users.
    - create: Creates a new user.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = []

    def get_queryset(self):
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(
                {
                    "detail": "Congratulations! Your account has been created successfully"
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    A view for handling user login.

    Methods:
    Inherits from TokenObtainPairView, which is a built-in view provided by the Django REST framework.
    """

    serializer_class = CustomTokenObtainPairSerializer

    # I will work on improving this later to include user activation and email verification using djoser
