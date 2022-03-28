from drf_yasg import openapi
from rest_framework import status

from . import sample_error_response


class SampleProfessionResponses:
    def __generate_sample_profession_response(self, status_code):
        """Generates sample response for profession response"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "professions": [
                        {
                            "id": 1,
                            "profession_name": "Software Engineer",
                        },
                        {
                            "id": 2,
                            "profession_name": "Software Tester",
                        },
                    ],
                }
            },
        )
        return response

    def __generate_sample_profession_detail_response(self, status_code):
        """Generates sample response for profession detail"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "profession": {
                        "id": 1,
                        "profession_name": "Software Engineer",
                    },
                }
            },
        )
        return response

    def get_all_profession_response(self):
        return {
            "200": self.__generate_sample_profession_response(status.HTTP_200_OK),
        }

    def get_profession_detail_response(self):
        return {
            "200": self.__generate_sample_profession_detail_response(
                status.HTTP_200_OK
            ),
            "400": sample_error_response.SampleErrorResponses().generate_sample_single_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
        }
