from django.http.response import JsonResponse
from rest_framework import status


def custom404(_, exception=None):
    """Returns custom 404 response"""
    return JsonResponse(
        {
            "code": status.HTTP_404_NOT_FOUND,
            "status": False,
            "error": "The URL requested could not be found",
        },
    )


def custom500(_):
    """Returns custom 500 response"""
    return JsonResponse(
        {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "status": False,
            "error": "Internal Server Error",
        }
    )
