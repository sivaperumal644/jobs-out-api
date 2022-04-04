from core.docs.sample_responses.sample_error_response import SampleErrorResponses
from drf_yasg import openapi
from rest_framework import status


class SampleUserResponses:
    def __generate_sample_token_response(self, status_code):
        """Generates sample response for token response"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "token": {
                        "access_token": "ACCESS_TOKEN",
                        "expires_in": 9899887878,
                        "refresh_token": "REFRESH_TOKEN,",
                    },
                    "user": {
                        "id": 1,
                        "user_id": "23e233dfd",
                        "email": "emailID",
                        "phone_number": "+91123456789",
                        "first_name": "name",
                        "last_name": "initial or last name",
                        "age": 18,
                        "gender": "M",
                        "profession": "profession",
                        "experience": 2,
                        "other_skills": "skills",
                        "is_admin": False,
                        "is_active": True,
                    },
                }
            },
        )
        return response

    def register_sample_response(self) -> dict:
        """Sample responses of register"""
        return {
            "201": self.__generate_sample_token_response(status.HTTP_201_CREATED),
            "400": SampleErrorResponses().generate_sample_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
        }

    def login_sample_response(self) -> dict:
        """Sample responses of login"""
        return {
            "200": self.__generate_sample_token_response(status.HTTP_200_OK),
            "400": SampleErrorResponses().generate_sample_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
            "401": SampleErrorResponses().generate_sample_error_response(
                status.HTTP_401_UNAUTHORIZED
            ),
        }

    def refresh_sample_response(self) -> dict:
        """Sample responses of refresh token"""
        return {
            "200": self.__generate_sample_token_response(status.HTTP_200_OK),
            "400": SampleErrorResponses().generate_sample_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
            "401": SampleErrorResponses().generate_sample_error_response(
                status.HTTP_401_UNAUTHORIZED
            ),
        }
