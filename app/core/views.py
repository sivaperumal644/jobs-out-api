from rest_framework import status
from rest_framework.response import Response


def custom404(request, exception=None):
    return Response(
        {
            "code": status.HTTP_404_NOT_FOUND,
            "status": False,
            "error": "The URL requested could not be found",
        },
        status=status.HTTP_404_NOT_FOUND,
    )
