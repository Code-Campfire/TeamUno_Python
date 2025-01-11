from django.db import models
from django.contrib.auth.models import User
from .post import Post
from .comment import Comment
from .friendship import Friendship

class NotificationType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField() #Metadata of what notification represents

class Notification(models.Model):

    user = models.ForeignKey(User on_delete=models.CASCADE) #recipient of notifications
    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    friendship = models.ForeignKey(
        Friendship,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    #should look into either deleting notifications after they are read, or maybe a periodic cleanup of old notifications. django post save could do it automatically, 
    # or we could archive, but then we would still be storing lots of notification objects.