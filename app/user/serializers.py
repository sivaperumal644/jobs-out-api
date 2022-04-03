from django.contrib import auth
from django.contrib.auth import get_user_model
from general.models import District, Profession, State
from rest_framework import serializers, status

from .models import User
from .utils import constants
from .utils.user_utils import (check_valid_email, check_valid_phone_number,
                               decode_jwt_token)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for registered User"""

    user_id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(
        max_length=255,
        min_length=8,
        required=True,
        error_messages=constants.EMAIL_ERROR_MESSAGES,
    )
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True,
        required=True,
        error_messages=constants.PASSWORD_ERROR_MESSAGES,
    )
    phone_number = serializers.CharField(
        max_length=13,
        required=True,
        error_messages=constants.PHONE_NUMBER_ERROR_MESSAGES,
    )
    first_name = serializers.CharField(
        max_length=255,
        min_length=2,
        required=True,
        error_messages=constants.FIRST_NAME_ERROR_MESSAGES,
    )
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    age = serializers.IntegerField(
        required=False, allow_null=True, error_messages=constants.GENDER_ERROR_MESSAGES
    )
    gender = serializers.ChoiceField(choices=User.gender_choices, required=False)
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        source="state",
    )
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        source="district",
    )
    profession_id = serializers.PrimaryKeyRelatedField(
        queryset=Profession.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
        source="profession",
    )
    experience = serializers.IntegerField(required=False, allow_null=True)
    other_skills = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    is_admin = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "user_id",
            "email",
            "password",
            "phone_number",
            "first_name",
            "last_name",
            "age",
            "gender",
            "profession",
            "profession_id",
            "state",
            "state_id",
            "district",
            "district_id",
            "experience",
            "other_skills",
            "is_admin",
            "is_active",
        ]
        depth = 1

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("User with this email already exists")
        if get_user_model().objects.filter(phone_number=attrs["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this phone number already exists"
            )
        return super().validate(attrs)

    def validate_email(self, value):
        if not check_valid_email(value):
            raise serializers.ValidationError("Your email format is invalid")
        return value

    def validate_phone_number(self, value):
        if not check_valid_phone_number(value):
            raise serializers.ValidationError("Enter a valid phone number")
        return value

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(**validated_data)
            return user
        except ValueError as error:
            return error


class LoginSerializer(serializers.Serializer):
    """Serializer for login API"""

    email = serializers.CharField(
        max_length=255,
        min_length=8,
        required=True,
        error_messages=constants.EMAIL_ERROR_MESSAGES,
    )
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True,
        required=True,
        error_messages=constants.PASSWORD_ERROR_MESSAGES,
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="User does not exist with this email",
                code=status.HTTP_400_BAD_REQUEST,
            )
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                detail="The credentials you entered are invalid",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for refresh token API"""

    refresh_token = serializers.CharField(
        max_length=255,
        required=True,
        error_messages=constants.REFRESH_TOKEN_ERROR_MESSAGES,
    )

    class Meta:
        model = User
        fields = ["refresh_token"]

    def validate(self, attrs):
        try:
            user_id = decode_jwt_token(attrs["refresh_token"])
            user = get_user_model().objects.filter(user_id=user_id).exists()

            if not user:
                raise serializers.ValidationError(
                    detail="Invalid token. User does not exist",
                    code=status.HTTP_401_UNAUTHORIZED,
                )

        except ValueError as error:
            raise serializers.ValidationError(
                detail=error, code=status.HTTP_401_UNAUTHORIZED
            )

        return super().validate(attrs)
