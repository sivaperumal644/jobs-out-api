from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from .models import User
from .utils import check_valid_email, check_valid_phone_number, decode_jwt_token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for registered User"""

    user_id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(
        max_length=255,
        min_length=8,
        required=True,
        error_messages={"min_length": "Email must be atleast 8 chararcters long"},
    )
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={"min_length": "Password must be atleast 8 chararcters long"},
    )
    phone_number = serializers.CharField(max_length=13, required=True)
    first_name = serializers.CharField(max_length=255, min_length=2, required=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=User.gender_choices, required=False)
    profession = serializers.CharField(max_length=50, required=False, allow_blank=True)
    experience = serializers.IntegerField(required=False, allow_null=True)
    other_skills = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = u"Email is required"
        self.fields["email"].error_messages["blank"] = u"Email is required"
        self.fields["email"].error_messages[
            "min_length"
        ] = u"Email must be atleast 8 characters long."
        self.fields["password"].error_messages["required"] = u"Password is required"
        self.fields["password"].error_messages["blank"] = u"Password is required"
        self.fields["phone_number"].error_messages[
            "required"
        ] = u"Phone Number is required"
        self.fields["phone_number"].error_messages[
            "blank"
        ] = u"Phone Number is required"
        self.fields["first_name"].error_messages["required"] = u"First name is required"
        self.fields["first_name"].error_messages["blank"] = u"First name is required"
        self.fields["gender"].error_messages[
            "invalid_choice"
        ] = u"{input} is not a valid gender choice"

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
            "experience",
            "other_skills",
        ]

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("User with this email already exists")
        if get_user_model().objects.filter(phone_number=attrs["phone_number"]).exists():
            raise serializers.ValidationError(
                "User with this phone number already exists"
            )
        if not check_valid_email(attrs["email"]):
            raise serializers.ValidationError("Your email format is invalid")
        if not check_valid_phone_number(attrs["phone_number"]):
            raise serializers.ValidationError("Enter a valid phone number")
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(**validated_data)
            return user
        except ValueError as error:
            return error


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for login API"""

    email = serializers.CharField(max_length=255, min_length=8, required=True)
    password = serializers.CharField(
        max_length=65,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={"min_length": "Password must be 8 chararcters long"},
    )

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = u"Email is required"
        self.fields["email"].error_messages["blank"] = u"Email is required"
        self.fields["password"].error_messages["required"] = u"Password is required"
        self.fields["password"].error_messages["blank"] = u"Password is required"

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="User does not exist with this email",
                code=status.HTTP_401_UNAUTHORIZED,
            )
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                detail="The credentials you entered are invalid",
                code=status.HTTP_401_UNAUTHORIZED,
            )
        return super().validate(attrs)


class RefreshTokenSerializer(serializers.ModelSerializer):
    """Serializer for refresh token API"""

    refresh_token = serializers.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(RefreshTokenSerializer, self).__init__(*args, **kwargs)
        self.fields["refresh_token"].error_messages[
            "required"
        ] = u"Refresh token is required"
        self.fields["refresh_token"].error_messages[
            "blank"
        ] = u"Refresh token is required"

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
