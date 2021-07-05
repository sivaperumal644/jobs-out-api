from drf_yasg import openapi


class SampleResponses:
    def sample_token_response(status_code):
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

    def sample_error_response(status_code):
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
