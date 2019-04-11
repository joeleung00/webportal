import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Message, GrepRequest
from .crawlpage import crawlpage, process_grep_requests
from django.contrib import messages #new added for popup message

from .check_err import check_no_repeat_name
from .check_err import check_input_error
from .ordering import reasign_order

def home(request):
    content = {}

    if request.user.is_authenticated:
        # dealing with categors
        # show category that is belongs to user
        categories = Category.objects.filter(author=request.user)

        content = {
            'category_blocks': None,
        }
        if "new_cate_title" in request.POST:
            if request.POST['new_cate_title'] != '':
                if (check_no_repeat_name(request, categories)):
                    new_category = Category()
                    new_category.title = request.POST['new_cate_title']
                    new_category.author = request.user
                    new_category.position = len(categories) + 1
                    new_category.save()
                    #add more so categories have been changed
                    categories = Category.objects.filter(author=request.user)

                else:
                    # raise the error message, the category name is repeated.
                    return HttpResponse("error")
            else:
                return HttpResponse("error")


        # dealing with grep request
        if "crawllink" in request.POST and "message_title" in request.POST and "crawltag" in request.POST:
            url = request.POST["crawllink"]
            msg_title = request.POST["message_title"]
            crawltag = request.POST["crawltag"]
            category_id = request.POST["category_dropdown"]
            add_to_calendar = request.POST["add_to_calendar"]

            #  checkvalid()..
            error = check_input_error(url, msg_title, crawltag, add_to_calendar, request.user)
            if ( error == 100):
                element = crawlpage(url, crawltag)
                # save message
                new_msg = Message()
                new_msg.title = msg_title
                new_msg.category = categories.get(pk = category_id)
                new_msg.content = element
                new_msg.save()

                # save grep request
                new_grep = GrepRequest()
                new_grep.content_title = msg_title
                new_grep.crawltag = crawltag
                if (add_to_calendar == '1'):
                    new_grep.add_to_calendar = True
                else:
                    new_grep.add_to_calendar = False
                new_grep.url = url
                new_grep.message = new_msg
                new_grep.save()
            else:
                return HttpResponse(error)



        content["category_blocks"] = [
            {
                'category': category,
                'messages': Message.objects.filter(category=category),
            } for category in categories
        ]

        # delete cate in the home page
        if "deleteCate" in request.POST:
            cate_id = request.POST["deleteCate"]
            print(cate_id)
            Category.objects.get(pk = cate_id).delete()


    return render(request, 'portal/home.html', content)



def about(request):
    process_grep_requests()
    return render(request, 'portal/about.html')



def category(request, pk):
    content = {}
    if request.user.is_authenticated:
        category = Category.objects.get(pk = pk)
        messages = Message.objects.filter(category__pk = pk)

        if "Delete_cate" in request.POST:

            category.delete()
            categories = Category.objects.filter(author=request.user)
            reasign_order(categories)
            return redirect('portal-home')

        if "Delete_msg" in request.POST:
            message_id = request.POST["Delete_msg"]
            Message.objects.get(pk=message_id).delete()

        if "Delete_multi_msg" in request.POST:
            messages_list = request.POST.getlist('selectedMessage[]')
            for message_id in messages_list:
                Message.objects.get(pk=message_id).delete()


    content = {
        'all_categories': Category.objects.filter(author=request.user),
        'category' : category,
        'messages': messages
    }
    return render(request, 'portal/category.html', content)

# Note that we are not afraid of identity forgery for recommendation
# as it is public, so we use csrf_exempt to exempt the identity check,
# For security-critical tasks, DO NOT blindly copy this tag.
@csrf_exempt
def recommend(request):
    reply = JsonResponse({'option': json.dumps([]), 'url': json.dumps([])})
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            if 'search_string' in json_data:
                search_string = json_data['search_string']
                grep_requests = GrepRequest.objects.filter(content_title__icontains=search_string)
                suggestions = [grep_request.content_title for grep_request in grep_requests]
                urls = [grep_request.url for grep_request in grep_requests]
                crawltags = [grep_request.crawltag for grep_request in grep_requests]
                # Generate at most 10 options
                #suggestions = ["CENG2010","CENG2400","ESTR2100","CENG3150","CENG3410","CENG3420"]
                #urls = ["a", "b", "c", "d", "e", "f"] # Auto filling URL is not implemented yet
                reply = JsonResponse({'option': json.dumps(suggestions), 'url': json.dumps(urls), 'crawltag': json.dumps(crawltags)})

    return reply
