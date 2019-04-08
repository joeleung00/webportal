from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message, GrepRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .crawlpage import crawlpage
from .tasks import process_grep_requests

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def check_no_repeat_name(request, categories):
    new_category_title = request.POST['new_cate_title']
    for category in categories:
        if (new_category_title == category.title):
            return False
    return True


def home(request):
    content = {}

    if request.user.is_authenticated:
        # dealing with categors
        # show category that is belongs to user
        categories = Category.objects.filter(author=request.user)

        content = {
            'category_blocks': None,
            'error': False
        }

        if "new_cate_title" in request.POST:

            if (check_no_repeat_name(request, categories)):
                new_category = Category()
                new_category.title = request.POST['new_cate_title']
                new_category.author = request.user
                new_category.save()
                #add more so categories have been changed
                categories = Category.objects.filter(author=request.user)
            else:
                # raise the error message, the category name is repeated.
                pass


        # dealing with grep request
        if "crawllink" in request.POST and "message_title" in request.POST and "crawltag" in request.POST:
            url = request.POST["crawllink"]
            msg_title = request.POST["message_title"]
            crawltag = request.POST["crawltag"]
            category_id = request.POST["category_dropdown"]
            #  checkvalid()...
            element = crawlpage(url, crawltag)

            # save message
            new_msg = Message()
            new_msg.title = msg_title
            new_msg.category = categories.get(pk = category_id)
            new_msg.content = ".."
            new_msg.save()

            # save grep request
            new_grep = GrepRequest()
            new_grep.content_title = msg_title
            new_grep.selected_content = element
            new_grep.url = url
            new_grep.message = new_msg
            new_grep.save()


        content["category_blocks"] = [
            {
                'category': category,
                'messages': Message.objects.filter(category=category),
            } for category in categories
        ]

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
            return redirect('portal-home')

        if "Delete_msg" in request.POST:
            message_id = request.POST["Delete_msg"]
            Message.objects.get(pk=message_id).delete()

        if "Delete_multi_msg" in request.POST:
            messages_list = request.POST.getlist['Delete_multi_msg']
            for message_id in messages_list:
                print ("message_id: ", message_id)
                Message.objects.get(pk=message_id).delete()


    content = {
        'category' : category,
        'messages': messages
    }
    return render(request, 'portal/category.html', content)


def google_calendar_connection():

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # Comment below three rows of code to require user to authorize everytime
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    return service

def calendar(request):
    content = {}

    Gcal = google_calendar_connection()

    # hard code insert events to calendar for testing
    GMT_OFF = '+08:00'      
    EVENT = {
        'summary': 'CSCI3100 HW',
        'start':  {'dateTime': '2019-04-07T16:30:00%s' % GMT_OFF},
        'end':    {'dateTime': '2019-04-07T17:00:00%s' % GMT_OFF},
    }

    e = Gcal.events().insert(calendarId='primary',sendNotifications=True, body=EVENT).execute()

    categories = Category.objects.filter(author=request.user)
    
    content = {
            'category_blocks': None,
            'error': False
        }

    content["category_blocks"] = [
            {
                'category': category,
                'messages': Message.objects.filter(category=category),
            } for category in categories
        ]

    return render(request, 'portal/home.html', content)
