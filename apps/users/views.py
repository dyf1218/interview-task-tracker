from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserMeSerializer, UserResponseSerializer


class RegisterView(APIView):
    """View for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = UserResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class MeView(APIView):
    """View for current user profile."""

    def get(self, request):
        """Return the current logged-in user."""
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)