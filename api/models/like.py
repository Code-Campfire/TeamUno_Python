from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .post import Post
from .comment import Comment

class Like(models.Model):
    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_given'
    )
    
    limit = models.Q(app_label='your_app', model='post') | \
            models.Q(app_label='your_app', model='comment')
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit
    )
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['liker', 'content_type', 'object_id'],
                name='unique_like'
            )
        ]
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def clean(self):
        # Check if content type is valid
        if not isinstance(self.related_object, (Post, Comment)):
            raise ValidationError("Content type must be either a Post or Comment")
        
        # Check for self-likes
        if hasattr(self.related_object, 'author'):
            if self.related_object.author == self.liker:
                raise ValidationError("Users cannot like their own content")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Like by {self.liker} on {self.content_type.name} {self.object_id}"