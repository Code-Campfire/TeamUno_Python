from django.db import models
from django.contrib.auth.models import User
from .post import Post



class Notification(models.Model):
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    #should look into either deleting notifications after they are read, or maybe a periodic cleanup of old notifications. django post save could do it automatically, 
    # or we could archive, but then we would still be storing lots of notification objects.
    # @receiver(post_save, sender=Notification)
    # def auto_delete_read_notifications(sender, instance, **kwargs):
    #     if instance.is_read:
    #         instance.delete()