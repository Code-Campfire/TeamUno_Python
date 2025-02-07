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
        fields = ('url', 'id', 'user', 'bio', 'birth_date', 'profile_picture')
        depth = 1

class Profiles(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)  # pylint: disable=no-member
            serializer = ProfileSerializer(profile, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def list(self, request):
        profiles = Profile.objects.all()  # pylint: disable=no-member
        serializer = ProfileSerializer(profiles, many=True, context={"request": request})
        return Response(serializer.data)