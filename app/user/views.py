from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import LoginSerializer, UserSerializer
from .utils import generate_jwt_token


class RegisterUserView(GenericAPIView):
    """Create a new user"""
    serializer_class = UserSerializer

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)

        if serialized_user.is_valid():
            serialized_user.save()
            token = generate_jwt_token(serialized_user.data)
            data = {
                'code': status.HTTP_201_CREATED,
                'status': True,
                'user': serialized_user.data,
                'token': token,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        errors = serialized_user.errors
        error = list(errors.values())[0][0]
        error_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'errors': errors,
            'error': error
        }
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


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
            payload = {
                'code': status.HTTP_200_OK,
                'status': True,
                'user': serialized_user.data,
                'token': token,
            }
            return Response(payload, status=status.HTTP_200_OK)

        errors = serialized_data.errors
        error = list(errors.values())[0][0]
        status_code = error.code
        if status_code is None or not isinstance(status_code, int):
            status_code = status.HTTP_400_BAD_REQUEST
        error_payload = {
            'code': status_code,
            'status': False,
            'errors': errors,
            'error': error
        }
        return Response(error_payload, status=status_code)
