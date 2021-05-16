from core.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .utils import check_valid_email, check_valid_phone_number


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for register User"""

    email = serializers.CharField(max_length=255, min_length=8, required=True)
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True, required=True, error_messages={
            "min_length": "Password must be 8 chararcters long"
        }
    )
    phone_number = serializers.CharField(max_length=13, required=True)
    first_name = serializers.CharField(
        max_length=255, min_length=2, required=True)
    last_name = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=User.gender_choices, required=False)
    profession = serializers.CharField(
        max_length=50, required=False, allow_blank=True)
    experience = serializers.IntegerField(required=False, allow_null=True)
    other_skills = serializers.CharField(
        max_length=255, required=False, allow_blank=True)

    def __init__(self, *args, **kwargs):
        super(RegisterUserSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['required'] = u"Email is required"
        self.fields['email'].error_messages['blank'] = u"Email is required"
        self.fields['password'].error_messages['required'] = u"Password is required"
        self.fields['password'].error_messages['blank'] = u"Password is required"
        self.fields['phone_number'].error_messages['required'] = u"Phone Number is required"
        self.fields['phone_number'].error_messages['blank'] = u"Phone Number is required"
        self.fields['first_name'].error_messages['required'] = u"First name is required"
        self.fields['first_name'].error_messages['blank'] = u"First name is required"
        self.fields['gender'].error_messages[
            'invalid_choice'] = u"{input} is not a valid gender choice"

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'phone_number', 'first_name', 'last_name', 'age',
                  'gender', 'profession', 'experience', 'other_skills']

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                'User with this email already exists')
        if get_user_model().objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError(
                'User with this phone number already exists')
        if not check_valid_email(attrs['email']):
            raise serializers.ValidationError(
                'Your email format is invalid')
        if not check_valid_phone_number(attrs['phone_number']):
            raise serializers.ValidationError('Enter a valid phone number')
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(**validated_data)
            return user
        except ValueError as error:
            return error
