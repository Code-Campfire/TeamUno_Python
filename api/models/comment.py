from django.db import models
from django.contrib.auth.models import User
from .post import Post



class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    # content is textfield for longer comments? not sure if we need real long comments or not.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
