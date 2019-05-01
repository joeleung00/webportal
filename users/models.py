from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# This model record the google calendar authentication of each user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_auth = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} Profile'

# This function will detect the user creation action
# The profile model will be created when any user is created
@receiver(post_save, sender=User)
def create_user_category(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
