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
        serialized_data = LoginSerializer(data=request.data)
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')

        if serialized_data.is_valid():
            if not get_user_model().objects.filter(email=email).exists():
                payload = {
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'status': False,
                    'error': 'User does not exist with this email'
                }

                return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

            user = auth.authenticate(email=email, password=password)

            if user:
                serialized_user = UserSerializer(user)

                token = generate_jwt_token(serialized_user.data)

                payload = {
                    'code': status.HTTP_200_OK,
                    'status': True,
                    'user': serialized_user.data,
                    'token': token,
                }

                return Response(payload, status=status.HTTP_200_OK)

            payload = {
                'code': status.HTTP_401_UNAUTHORIZED,
                'status': False,
                'error': 'The credentials you entered are invalid'
            }

            return Response(payload, status=status.HTTP_401_UNAUTHORIZED)

        errors = serialized_data.errors
        error = list(errors.values())[0][0]
        error_payload = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'errors': errors,
            'error': error
        }
        return Response(error_payload, status=status.HTTP_400_BAD_REQUEST)
