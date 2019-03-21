from django.contrib import admin
from .models import Message
from .models import Category

admin.site.register(Message)
admin.site.register(Category)
