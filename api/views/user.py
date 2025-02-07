from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from .profile import ProfileSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name="user-detail", 
            lookup_field="pk"  
        )
        fields = (
            "id",
            "url",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_staff"
        )

class UserWithProfileSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(required=False)  # Made optional
    
    class Meta:
        model = User  
        url = serializers.HyperlinkedIdentityField(
            view_name="user-detail",
            lookup_field="pk"
        )
        fields = (
            "id",
            "url",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "profile"
        )

class Users(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            # No need to fetch profile separately - serializer will handle it
            serializer = UserWithProfileSerializer(user, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)