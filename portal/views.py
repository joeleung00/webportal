from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message, GrepRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .crawlpage import crawlpage
from .tasks import process_grep_requests

def home(request):
    content = {}

    if request.user.is_authenticated:
        # dealing with categors
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

        # dealing with grep request
        if "crawllink" in request.POST and "message_title" in request.POST and "crawltag" in request.POST:
            url = request.POST["crawllink"]
            msg_title = request.POST["message_title"]
            crawltag = request.POST["crawltag"]
            category_name = request.POST["category"]
            #  checkvalid()...
            element = crawlpage(url, crawltag)

            new_grep = GrepRequest()
            new_grep.content_title = msg_title
            new_grep.selected_content = element
            new_grep.url = url

            new_msg = Message()
            new_msg.title = msg_title
            new_msg.category = categories.get(title = category_name)
            new_msg.content = ".."
            new_msg.save()

            new_grep.message = new_msg
            new_grep.save()





        category_blocks = [
            {
                'category': category,
                'messages': Message.objects.filter(category=category),
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
