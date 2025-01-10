from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Friendship(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    # added related name to make it easier to query in django
    requesting_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent'
    )
    requested_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.requesting_id == self.requested_id:
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