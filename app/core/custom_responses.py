from rest_framework import status
from rest_framework.response import Response


class CustomResponses:
    def error_response(errors):
        """Return Error response for given data"""
        error = list(errors.values())[0][0]
        status_code = error.code
        if status_code is None or not isinstance(status_code, int):
            status_code = status.HTTP_400_BAD_REQUEST
        error_payload = {
            "code": status_code,
            "status": False,
            "errors": errors,
            "error": error,
        }
        return Response(error_payload, status=status_code)

    def single_error_response(error, status_code=status.HTTP_400_BAD_REQUEST):
        """Return custom error response"""
        error_payload = {
            "code": status_code,
            "status": False,
            "error": error,
        }
        return Response(error_payload, status=status_code)

    def token_response(token, user, status_code=status.HTTP_200_OK):
        """Returns response of token and user"""
        data = {
            "code": status_code,
            "status": True,
            "user": user,
            "token": token,
        }
        return Response(data, status=status_code)

    def get_states_response(states, status_code=status.HTTP_200_OK):
        """Returns response of list of available states"""
        data = {
            "code": status_code,
            "status": True,
            "states": states,
        }
        return Response(data, status=status_code)

    def get_state_response(state, status_code=status.HTTP_200_OK):
        """Returns response of given state"""
        data = {
            "code": status_code,
            "status": True,
            "state": state,
        }
        return Response(data, status=status_code)

    def get_districts_response(districts, status_code=status.HTTP_200_OK):
        """Returns response of list of available districts"""
        data = {
            "code": status_code,
            "status": True,
            "districts": districts,
        }
        return Response(data, status=status_code)

    def get_district_response(district, status_code=status.HTTP_200_OK):
        """Returns response of given district"""
        data = {
            "code": status_code,
            "status": True,
            "district": district,
        }
        return Response(data, status=status_code)

    def get_professions_response(professions, status_code=status.HTTP_200_OK):
        """Returns response of list of available professions"""
        data = {
            "code": status_code,
            "status": True,
            "professions": professions,
        }
        return Response(data, status=status_code)

    def get_profession_response(profession, status_code=status.HTTP_200_OK):
        """Returns response of given profession"""
        data = {
            "code": status_code,
            "status": True,
            "profession": profession,
        }
        return Response(data, status=status_code)
