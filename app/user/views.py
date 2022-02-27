from core.custom_responses import CustomResponses
from core.docs.sample_responses.sample_user_response import SampleUserResponses
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from .serializers import LoginSerializer, RefreshTokenSerializer, UserSerializer
from .utils.user_utils import decode_jwt_token, generate_jwt_token


class RegisterUserView(GenericAPIView):
    """Create a new user"""

    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses=SampleUserResponses().refresh_sample_response(),
        request_body=UserSerializer,
    )
    def post(self, request):
        serialized_user = UserSerializer(data=request.data)

        if serialized_user.is_valid():
            serialized_user.save()
            token = generate_jwt_token(serialized_user.data)
            return CustomResponses.token_response(
                token, serialized_user.data, status_code=status.HTTP_201_CREATED
            )

        return CustomResponses.error_response(serialized_user.errors)


class LoginUserView(GenericAPIView):
    """Login a user and get jwt token"""

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        responses=SampleUserResponses().login_sample_response(),
        request_body=LoginSerializer,
    )
    def post(self, request):
        data = request.data
        serialized_data = LoginSerializer(data=data)
        email = data.get("email", "")

        if serialized_data.is_valid():
            user = get_user_model().objects.get(email=email)
            serialized_user = UserSerializer(user)
            token = generate_jwt_token(serialized_user.data)
            return CustomResponses.token_response(token, serialized_user.data)

        return CustomResponses.error_response(serialized_data.errors)


class RefreshTokenView(GenericAPIView):
    "Get refresh token and send a fresh access and refresh token"
    serializer_class = RefreshTokenSerializer

    @swagger_auto_schema(
        responses=SampleUserResponses().refresh_sample_response(),
        request_body=RefreshTokenSerializer,
    )
    def post(self, request):
        data = request.data
        serialized_data = RefreshTokenSerializer(data=data)
        refresh_token = data.get("refresh_token", "")

        if serialized_data.is_valid():
            user_id = decode_jwt_token(refresh_token)
            user = get_user_model().objects.get(user_id=user_id)
            serialized_user = UserSerializer(user)
            token = generate_jwt_token(serialized_user.data)
            return CustomResponses.token_response(token, serialized_user.data)

        return CustomResponses.error_response(serialized_data.errors)
