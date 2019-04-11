from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    title = models.CharField(max_length=100)
    author =  models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']

class Message(models.Model):
    # This would be used for storing GrepReply
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    full_url = models.CharField(max_length=500, default='')
    #date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-modified_date']

class GrepRequest(models.Model):
    content_title = models.CharField(max_length=100)
    crawltag = models.TextField(default='test')
    #selector_type = models.CharField(max_length=5)
    url = models.CharField(max_length=500)
    #date_posted = models.DateTimeField(default=timezone.now)
    add_to_calendar = models.BooleanField(default=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return self.content_title

@receiver(post_save, sender=User)
def create_user_category(sender, instance, created, **kwargs):
    if created:
        Category.objects.create(author=instance, title="News")
