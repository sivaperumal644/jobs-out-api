from core.custom_responses import CustomResponses
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from core.docs.sample_response import SampleResponses

from .serializers import LoginSerializer, RefreshTokenSerializer, UserSerializer
from .utils import decode_jwt_token, generate_jwt_token

# For Sample response in swagger docs.
register_sample_response = {
    "201": SampleResponses.sample_token_response(status_code=status.HTTP_201_CREATED),
    "400": SampleResponses.sample_error_response(
        status_code=status.HTTP_400_BAD_REQUEST
    ),
}

login_sample_response = {
    "200": SampleResponses.sample_token_response(status_code=status.HTTP_200_OK),
    "400": SampleResponses.sample_error_response(
        status_code=status.HTTP_400_BAD_REQUEST
    ),
    "401": SampleResponses.sample_error_response(
        status_code=status.HTTP_401_UNAUTHORIZED
    ),
}

refresh_sample_response = {
    "200": SampleResponses.sample_token_response(status_code=status.HTTP_200_OK),
    "400": SampleResponses.sample_error_response(
        status_code=status.HTTP_400_BAD_REQUEST
    ),
    "401": SampleResponses.sample_error_response(
        status_code=status.HTTP_401_UNAUTHORIZED
    ),
}


class RegisterUserView(GenericAPIView):
    """Create a new user"""

    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses=register_sample_response, request_body=UserSerializer
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

    @swagger_auto_schema(responses=login_sample_response, request_body=LoginSerializer)
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
        responses=refresh_sample_response, request_body=RefreshTokenSerializer
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
