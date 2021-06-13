from core.custom_responses import error_response, token_response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .serializers import (LoginSerializer, RefreshTokenSerializer,
                          UserSerializer)
from .utils import decode_jwt_token, generate_jwt_token


class RegisterUserView(GenericAPIView):
    """Create a new user"""
    serializer_class = UserSerializer

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)

        if serialized_user.is_valid():
            serialized_user.save()
            token = generate_jwt_token(serialized_user.data)
            return token_response(token, serialized_user.data, status_code=status.HTTP_201_CREATED)

        return error_response(serialized_user.errors)


class LoginUserView(GenericAPIView):
    """Login a user and get jwt token"""
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serialized_data = LoginSerializer(data=data)
        email = data.get('email', '')

        if serialized_data.is_valid():
            user = get_user_model().objects.get(email=email)
            serialized_user = UserSerializer(user)
            token = generate_jwt_token(serialized_user.data)
            return token_response(token, serialized_user.data)

        return error_response(serialized_data.errors)


class RefreshTokenView(GenericAPIView):
    "Get refresh token and send a fresh access and refresh token"
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        data = request.data
        serialized_data = RefreshTokenSerializer(data=data)
        refresh_token = data.get('refresh_token', '')

        if serialized_data.is_valid():
            user_id = decode_jwt_token(refresh_token)
            user = get_user_model().objects.get(user_id=user_id)
            serialized_user = UserSerializer(user)
            token = generate_jwt_token(serialized_user.data)
            return token_response(token, serialized_user.data)

        return error_response(serialized_data.errors)
