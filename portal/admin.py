from django.contrib import admin
from .models import Message
from .models import Category
from .models import GrepRequest

# We register Message, Category and GrepRequest model so that we can use admin page the directly access it.
admin.site.register(Message)
admin.site.register(Category)
admin.site.register(GrepRequest)
