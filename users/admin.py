from django.contrib import admin
from .models import Profile
# Register Profile models for direct access in admin page.
admin.site.register(Profile)
