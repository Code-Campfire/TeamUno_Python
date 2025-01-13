from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
# Add pylint: disable=unused-argument to ignore the unused sender and kwargs parameters
# These parameters are required by Django's signal system even if we don't use them
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        Profile.objects.create(user=instance) # pylint: disable=no-member

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  # pylint: disable=unused-argument
    instance.profile.save()