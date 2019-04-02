from django.contrib import admin
from .models import Message
from .models import Category
from .models import GrepRequest

admin.site.register(Message)
admin.site.register(Category)
admin.site.register(GrepRequest)
