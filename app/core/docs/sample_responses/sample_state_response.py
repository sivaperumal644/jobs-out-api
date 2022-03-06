from drf_yasg import openapi
from rest_framework import status


class SampleStateResponses:
    def __generate_sample_state_response(self, status_code):
        """Generates sample response for state response"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "states": {
                        "id": 1,
                        "state_name": "State Name",
                    },
                }
            },
        )
        return response

    def get_all_states_response(self):
        return {
            "200": self.__generate_sample_state_response(status.HTTP_200_OK),
        }
