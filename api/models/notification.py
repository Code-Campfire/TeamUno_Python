from django.db import models
from django.contrib.auth.models import User
from .post import Post
from .comment import Comment
from .friendship import Friendship



class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('FRIEND_REQUEST', 'Friend Request'),
        ('COMMENT', 'Comment'),
        ('COMMENT_REPLY', 'Comment Reply'),
    ]
    user = models.ForeignKey(User on_delete=models.CASCADE) #recipient of notifications
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
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