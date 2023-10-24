from django.core import validators
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer includes fields for the user's email, password, and phone number,
    as well as the standard fields for the User model (id and username). The email field
    is validated to ensure that it is a valid email address and is unique. The password
    field is write-only and requires a minimum length of 8 characters. The phone field
    is validated to ensure that it is a valid Nigerian phone number.

    The create() method is overridden to create a new user with the validated data.
    """

    email = serializers.EmailField(
        validators=[
            validators.EmailValidator(message="Provide a valid email address"),
            UniqueValidator(
                queryset=User.objects.all(), message="Email already exists"
            ),
        ],
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
    )
    phone = serializers.CharField(
        validators=[
            validators.RegexValidator(
                regex=r"^\+?(234)?[789][01]\d{8}$",
                message="Provide a valid nigerian phone number",
            ),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "phone",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer:
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email does not exist")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining a JSON Web Token.

    Inherits from TokenObtainPairSerializer and adds custom claims to the token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.email
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = self.user.email
        data["user_id"] = self.user.id

        return data
