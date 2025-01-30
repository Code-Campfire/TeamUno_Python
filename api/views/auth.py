from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from django.contrib.auth import login

from api.serializers.auth_serializers import SignupSerializer, LoginSerializer, LogoutSerializer, SessionSerializer


class AuthViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def signup(self, request):
        """
        User signup creates a new user in the system.

        Validates the request data and creates a user with the provided
        username, email, and password. Automatically creates a profile for the user.

        Args:
            request (Request): The HTTP request containing user data.

        Returns:
            Response: A response object with a success message if the user is created,
            or validation errors if the input is invalid.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            (
                serializer.save()
            )  # Save calls create in serializer, create is create_user, password automatically hashed.
            return Response(
                {"message": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Authenticates a user and starts a session.

        Validates the username and password provided in the request.
        If the credentials are valid, logs in the user and creates a session.

        Args:
            request (Request): The HTTP request containing login data (username and password).

        Returns:
            Response: A response object with a success message if authentication is successful,
            or an error message if the credentials are invalid.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  
            login(request, user)  # Log the user in (sets the session)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=["post"])
    def logout(self, request):
        """
        Logs out the current user and ends the session.

        Clears the session data for the authenticated user. Requires the session ID
        and CSRF token to be sent with the request.

        Args:
            request (Request): The HTTP request containing session and CSRF information.

        Returns:
            Response: A response object confirming the user has been logged out.
        """
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # This will flush the session
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def check_session(self, request):
        """
        Checks if the user is authenticated via the saved session.
        serializer returns the user ID and username.
        """
        serializer = SessionSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    