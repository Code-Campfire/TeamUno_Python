from django.http import HttpResponseServerError
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from api.models import Friendship, statustypes

class FriendshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friendship
        url = serializers.HyperlinkedIdentityField(
            view_name='friendship_detail', lookup_field='id'
        )
        fields= ('requesting', 'requested', 'created_at', 'updated_at', 'status')
        depth = 1

class Friendships(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            friendship = Friendship.objects.get(pk=pk)  # pylint: disable=no-member
            serializer = FriendshipSerializer(friendship, context={"request": request})
            return Response(serializer.data)
        except Exception as ex: 
            return HttpResponseServerError(ex)
    def list(self, request):
        try:
            friendship = Friendship.objects.all() # pylint: disable=no-member
            serializer = FriendshipSerializer(friendship, many=True, context={"request": request})
            return Response(serializer.data)
        except Exception as ex: 
            return HttpResponseServerError(ex)
    def create(self, request):
        new_friendship= Friendship()
        new_friendship.requesting = request.auth.user
        new_friendship.requested = request.data["requested"]
        new_friendship.created_at = datetime.datetime.now()
        new_friendship.updated_at = None
        new_friendship.status = 'PENDING'
        new_friendship.save()

        serializer = FriendshipSerializer(
           new_friendship, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)