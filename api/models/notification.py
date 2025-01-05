from django.db import models
from django.contrib.auth.models import User
from .post import Post



class Notification(models.Model):
    post_id = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING
    )
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    is_read = models.BooleanField()