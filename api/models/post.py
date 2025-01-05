from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    author_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
