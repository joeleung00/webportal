from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message
from django.contrib.auth.models import User

from .tasks import process_grep_requests

def home(request):
    content = {}

    if request.user.is_authenticated:
        categories = Category.objects.filter(author=request.user)
        category_blocks = [
            {
                'category': category
                'messages': Message.objects.filter(category=category)
            } for category in categories
        ]
        content = {
            'category_blocks': category_blocks
        }

    return render(request, 'portal/home.html', content)

def about(request):
    return render(request, 'portal/about.html')


def category(request, pk):
    process_grep_requests()
    content = {}
    if request.user.is_authenticated:
        category = Category.objects.get(pk = pk)
        messages = Message.objects.filter(category__pk = pk)
        content = {
            'category' : category,
            'messages': messages
        }

    return render(request, 'portal/category.html', content)
