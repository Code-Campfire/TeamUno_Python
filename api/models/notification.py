from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class NotificationType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    # Template for formatting notification messages
    template = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = 'Notification Type'
        verbose_name_plural = 'Notification Types'

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.PROTECT
    )
    # Generic foreign key to link to any model (Post, Comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    #should look into either deleting notifications after they are read, or maybe a periodic cleanup of old notifications. django post save could do it automatically, 
    # or we could archive, but then we would still be storing lots of notification objects.
    # @receiver(post_save, sender=Notification)
    # def auto_delete_read_notifications(sender, instance, **kwargs):
    #     if instance.is_read:
    #         instance.delete()