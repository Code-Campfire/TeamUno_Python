from django.db import models
from django.contrib.auth.models import User
from .post import Post



class Comment(models.Model):
    # changed models to cascade on deletion of post or commenter 
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    commenter_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    # content is textfield for longer comments? not sure if we need real long comments or not.
    content = models.TextField()
    # auto now will add current dates and times when object is created or updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
