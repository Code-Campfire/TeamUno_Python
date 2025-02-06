from django.http import HttpResponseServerError
from django.db.models import Q 
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from api.models import Friendship, StatusTypes

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        url = serializers.HyperlinkedIdentityField(
            view_name='friendship_detail', lookup_field='id'
        )
        fields = ('id', 'requesting', 'requested', 'created_at', 'updated_at', 'status')
        read_only_fields = ('requesting', 'created_at', 'updated_at')
        depth = 1

class Friendships(ViewSet):
    def get_queryset(self):
        """
        Filter friendships based on the authenticated user
        """
        user = self.request.user
        return Friendship.objects.filter( # pylint: disable=no-member
            Q(requesting=user) | Q(requested=user)
            )
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
