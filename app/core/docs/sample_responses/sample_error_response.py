from drf_yasg import openapi


class SampleErrorResponses:
    def generate_sample_error_response(self, status_code):
        """Generates sample response for errors"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": False,
                    "errors": {
                        "key1": ["key1 is required"],
                        "key2": ["key2 is required"],
                    },
                    "error": "key1 is required",
                }
            },
        )
        return response

    def generate_sample_single_error_response(self, status_code):
        """Generates sample response for single error"""
        response = openapi.Response(
            description=f"Example of {status_code} Response",
            examples={
                "application/json": {
                    "code": status_code,
                    "status": False,
                    "error": "Data not available",
                }
            },
        )
        return response
