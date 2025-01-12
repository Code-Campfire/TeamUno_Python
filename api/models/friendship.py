from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .statustypes import StatusTypes


class Friendship(models.Model):
    # added related name to make it easier to query in django
    requesting = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent'
    )
    requested = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(
        StatusTypes,
        on_delete=models.PROTECT
    )

    def save(self, *args, **kwargs):
        if self.requesting == self.requested:
            raise ValidationError("User cannot send friendship requests to themselves.")
        super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['requesting_id', 'requested_id'],
                name='unique_friendship'
            ),
            models.UniqueConstraint(
                fields=['requested_id', 'requesting_id'],
                name='unique_reverse_friendship'
            )
        ]