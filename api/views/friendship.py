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
    def create(self, request):
        try:
            # Get or create pending status
            pending_status = StatusTypes.objects.get(status='PENDING') # pylint: disable=no-member
            
            friendship = Friendship(
                requesting=request.user,
                requested_id=request.data.get('requested'),
                status=pending_status
            )
            
            # This will trigger the model's save validation
            friendship.save()
            
            serializer = self.get_serializer(friendship)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            return Response(
                {"detail": "Friendship request already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Failed to create friendship request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def update(self, request, pk=None):
        friendship = get_object_or_404(Friendship, pk=pk)
        
        # Only the requested user can update the friendship status
        if request.user != friendship.requested:
            return Response(
                {"detail": "Only the requested user can update friendship status"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            new_status = StatusTypes.objects.get(status=request.data.get('status', '').upper())
            friendship.status = new_status
            friendship.save()
            
            serializer = self.get_serializer(friendship)
            return Response(serializer.data)
            
        except StatusTypes.DoesNotExist:
            return Response(
                {"detail": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )