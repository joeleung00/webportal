from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message, GrepRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect

# When some category was deleted, there are some gap in the category position. eg 1 3 4 5 ...
# when category with position 2 was deleted.
# This reasign_order function will fill the gap
def reasign_order(categories):
    for i, category in enumerate(categories):
        category.position = i + 1
        category.save()

# after receiving the category order sent by user, we update the position attribute for each category.
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
