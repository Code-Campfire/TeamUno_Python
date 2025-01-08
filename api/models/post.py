from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)