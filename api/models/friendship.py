from django.db import models
from django.contrib.auth.models import User


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
    requesting_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    requested_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()