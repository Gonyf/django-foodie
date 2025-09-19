from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = bio = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if UserProfile.objects.filter(user=instance).exists():
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)