import datetime
import re

import jwt
from django.conf import settings


def generate_jwt_token(user):
    """Generates access token and refresh token for the given user"""
    access_token_expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    epoch = datetime.datetime.utcfromtimestamp(0)
    access_token_payload = {
        'user_id': user['email'],
        'exp': access_token_expiry_time,
        'iat': datetime.datetime.utcnow()
    }

    refresh_token_payload = {
        'user_id': user['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),
        'iat': datetime.datetime.utcnow()
    }

    access_token = jwt.encode(
        access_token_payload, settings.TOKEN_SECRET_KEY, algorithm='HS256').decode('utf-8')

    refresh_token = jwt.encode(
        refresh_token_payload, settings.TOKEN_SECRET_KEY, algorithm='HS256').decode('utf-8')

    response = {
        'access_token': access_token,
        'expires_in': int((access_token_expiry_time - epoch).total_seconds()) * 1000,
        'refresh_token': refresh_token
    }

    return response

# ^([0]|\+91)[789]\d{9}$


def check_valid_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    return False


def check_valid_phone_number(phone_number):
    regex = "^\+91[6-9]{1}[0-9]{9}$"

    if(re.search(regex, phone_number)):
        return True
    return False
