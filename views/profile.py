from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from api.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Participants"""
    class Meta:
        model = Profile
        url = serializers.HyperlinkedIdentityField(
            view_name='profile_detail', lookup_field='id'
        )
        fields = ('url', 'id', 'user', 'bio', 'birthdate', 'profile_picture')
        depth = 1

class Profiles(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)