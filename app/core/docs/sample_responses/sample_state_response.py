from drf_yasg import openapi
from rest_framework import status

from . import sample_error_response


class SampleStateResponses:
    def __generate_sample_states_response(self, status_code):
        """Generates sample response for state response"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "states": [
                        {
                            "id": 1,
                            "state_name": "State Name 1",
                        },
                        {
                            "id": 2,
                            "state_name": "State Name 2",
                        },
                    ],
                }
            },
        )
        return response

    def __generate_sample_state_detail_response(self, status_code):
        """Generates sample response for state detail"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "state": {
                        "id": 1,
                        "state_name": "State Name 1",
                    },
                }
            },
        )
        return response

    def get_all_states_response(self):
        """Sample response for all states"""
        return {
            "200": self.__generate_sample_states_response(status.HTTP_200_OK),
        }

    def get_state_detail_response(self):
        """Sample response for state detail"""
        return {
            "200": self.__generate_sample_state_detail_response(status.HTTP_200_OK),
            "400": sample_error_response.SampleErrorResponses().generate_sample_single_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
        }
