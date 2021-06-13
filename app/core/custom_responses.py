from rest_framework import status
from rest_framework.response import Response


def error_response(errors):
    """Return Error response for given data"""
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


def token_response(token, user, status_code=status.HTTP_200_OK):
    """Returns response of token and user"""
    data = {
        'code': status_code,
        'status': True,
        'user': user,
        'token': token,
    }
    return Response(data, status=status_code)
