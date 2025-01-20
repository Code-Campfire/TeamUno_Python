from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .profile import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Participants"""
    class Meta:
        model = Profile
        url = serializers.HyperlinkedIdentityField(
            view_name='Profile', lookup_field='id'
        )
        fields = ('id', 'user', 'bio', 'birthdate', 'profilepicture')
        depth = 1

class Participants(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            participant = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(participant, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)