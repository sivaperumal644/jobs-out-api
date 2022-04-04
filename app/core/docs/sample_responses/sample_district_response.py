from drf_yasg import openapi
from rest_framework import status

from . import sample_error_response


class SampleDistrictResponses:
    def __generate_sample_districts_response(self, status_code):
        """Generates sample response for districts response"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "districts": [
                        {
                            "id": 1,
                            "district_name": "District Name 1",
                            "state_id": 1,
                        },
                        {
                            "id": 2,
                            "district_name": "District Name 1",
                            "state_id": 1,
                        },
                    ],
                }
            },
        )
        return response

    def __generate_sample_district_detail_response(self, status_code):
        """Generates sample response for district detail"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": True,
                    "district": {
                        "id": 1,
                        "state_name": "State Name 1",
                    },
                }
            },
        )
        return response

    def get_all_districts_response(self):
        """Sample response for all districts"""
        return {
            "200": self.__generate_sample_districts_response(status.HTTP_200_OK),
        }

    def get_district_detail_response(self):
        """Sample response for district detail"""
        return {
            "200": self.__generate_sample_district_detail_response(status.HTTP_200_OK),
            "400": sample_error_response.SampleErrorResponses().generate_sample_single_error_response(
                status.HTTP_400_BAD_REQUEST
            ),
        }
