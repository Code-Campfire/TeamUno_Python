from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.

    Validates the input data and creates a new user in the system. Ensures that
    the username and email are unique and that the password meets the minimum length.
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """
        Meta options for SignupSerializer.

        Defines the model and fields that should be included in serialization.
        """

        model = User
        fields = ["username", "email", "password"]

    def validate_email(self, value):
        """
        Check if the email is already registered.

        Args:
            value (str): The email value being validated.

        Returns:
            str: The validated email if it is unique.

        Raises:
            serializers.ValidationError: If the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates the username and password provided by the user. Authenticates
    the user and returns the validated user object.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        return user


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.

    No input fields required, but uses request context to clear a user session.
    Terminates session and raises error if no active session found.
    """

    def save(self, **kwargs):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            request.session.flush()
        else:
            raise serializers.ValidationError("No user logged in.")

class SessionSerializer(serializers.ModelSerializer):
    """
    Serializer for returning authenticated user session
    """
    class Meta:
        model = User
        fields = ["id", "username"]
