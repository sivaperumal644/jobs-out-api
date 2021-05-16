from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
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
