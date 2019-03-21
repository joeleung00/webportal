from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    author =  models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Message(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class GrepRequest(models.Model):
    # title = models.CharField(max_length=100)
    # content = ...
    #url = models.CharField(max_length=100)
    #content_title = models.CharField(max_length=100)
    #selected_content = models.TextField()

    def __str__(self):
        return self.content_title
