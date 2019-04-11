from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message, GrepRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect

def reasign_order(categories):
    for i, category in enumerate(categories):
        category.position = i + 1
        category.save()

def reorder(request):
    categories = Category.objects.filter(author=request.user)

    if "order[]" in request.POST:
        order = request.POST.getlist('order[]')
        for i, id in enumerate(order):
            category = categories.get(pk = id)
            category.position = i + 1
            category.save()
        categories.order_by('position')

    return redirect('portal-home')
