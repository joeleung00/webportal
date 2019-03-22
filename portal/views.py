from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message
from django.contrib.auth.models import User
from django.shortcuts import redirect
def home(request):
    content = {}

    if request.user.is_authenticated:
        # show category that is belongs to user
        categories = Category.objects.filter(author=request.user)


        if "new_cate_title" in request.POST:
            should_add = True
            new_category_name = request.POST['new_cate_title']
            for category in categories:
                if (new_category_name == category.title):
                    should_add = False

            if (should_add):
                new_category = Category()
                new_category.title = new_category_name
                new_category.author = request.user
                new_category.save()
                #add more so categories have been changed
                categories = Category.objects.filter(author=request.user)


        content = {
            'categories': categories
        }
    return render(request, 'portal/home.html', content)

def about(request):
    return render(request, 'portal/about.html')


def category(request, pk):
    content = {}
    if request.user.is_authenticated:
        category = Category.objects.get(pk = pk)
        messages = Message.objects.filter(category__pk = pk)

        if "Delete_cate" in request.POST:
            category.delete()
            return redirect('portal-home')

        if "Delete_msg" in request.POST:
            message_id = request.POST["Delete_msg"]
            Message.objects.get(pk=message_id).delete()

    content = {
        'category' : category,
        'messages': messages
    }
    return render(request, 'portal/category.html', content)
