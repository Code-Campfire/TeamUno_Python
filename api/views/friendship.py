from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from api.models import Friendship, StatusTypes
from rest_framework import serializers

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('id', 'requesting', 'requested', 'created_at', 'updated_at', 'status')
        read_only_fields = ('requesting', 'created_at', 'updated_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add additional user details
        representation['requesting'] = {
            'id': instance.requesting.id,
            'username': instance.requesting.username,
        }
        representation['requested'] = {
            'id': instance.requested.id,
            'username': instance.requested.username,
        }
        return representation

class Friendships(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()  # pylint: disable=no-member
    serializer_class = FriendshipSerializer
    
    def get_queryset(self):
        """
        Filter friendships based on the authenticated user
        """
        user = self.request.user
        
        # Filter by status if provided in query params
        status_filter = self.request.query_params.get('status', None)
        queryset = Friendship.objects.filter(  # pylint: disable=no-member
            Q(requesting=user) | Q(requested=user)
        )
        
        if status_filter:
            queryset = queryset.filter(status__status=status_filter.upper())
            
        return queryset
    
    def create(self, request):
        try:
            # Get pending status
            pending_status = StatusTypes.objects.get(status='PENDING')  # pylint: disable=no-member
            
            # Validate the input data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Save with the requesting user and status
            friendship = serializer.save(
                requesting=request.user,
                status=pending_status
            )
            
            return Response(
                self.get_serializer(friendship).data, 
                status=status.HTTP_201_CREATED
            )
            
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
        except StatusTypes.DoesNotExist: # pylint: disable=no-member
            return Response(
                {"detail": "Pending status type not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"detail": f"Failed to create friendship request: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, pk=None):
        friendship = self.get_object()
        
        # Only the requested user can update the friendship status
        if request.user != friendship.requested:
            return Response(
                {"detail": "Only the requested user can update friendship status"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            new_status = StatusTypes.objects.get(status=request.data.get('status', '').upper())  # pylint: disable=no-member
            friendship.status = new_status
            friendship.save()
            
            serializer = self.get_serializer(friendship)
            return Response(serializer.data)
            
        except StatusTypes.DoesNotExist: # pylint: disable=no-member
            return Response(
                {"detail": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a friend request"""
        friendship = self.get_object()
        if request.user != friendship.requested:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            accepted_status = StatusTypes.objects.get(status='ACCEPTED')  # pylint: disable=no-member
            friendship.status = accepted_status
            friendship.save()
            serializer = self.get_serializer(friendship)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a friend request"""
        friendship = self.get_object()
        if request.user != friendship.requested:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            rejected_status = StatusTypes.objects.get(status='REJECTED')  # pylint: disable=no-member
            friendship.status = rejected_status
            friendship.save()
            serializer = self.get_serializer(friendship)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Terminate an existing friendship"""
        friendship = self.get_object()
        if request.user not in [friendship.requesting, friendship.requested]:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            terminated_status = StatusTypes.objects.get(status='TERMINATED')  # pylint: disable=no-member
            friendship.status = terminated_status
            friendship.save()
            serializer = self.get_serializer(friendship)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)