from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message, GrepRequest
from django.shortcuts import redirect
from users.models import Profile

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def google_calendar_connection():

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # Comment below three rows of code to require user to authorize everytime
    try:
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
    except:
        return False

    return service

def createEvent(Gcal, title, startDate, startTime, endDate, endTime):

    # HK timezone
    GMT_OFF = '+08:00'

    EVENT = {
        'summary': title,
        'start':  {'dateTime': '%sT%s%s' % (startDate, startTime, GMT_OFF)},
        'end':    {'dateTime': '%sT%s%s' % (endDate, endTime, GMT_OFF)},
    }

    e = Gcal.events().insert(calendarId='primary',sendNotifications=True, body=EVENT).execute()

def calendar(request):

    Gcal = google_calendar_connection()
    if (Gcal != False):
        profile = Profile.objects.get(user=request.user)
        profile.google_auth = True
        profile.save()


    # example of calling createEvent function
    #createEvent(Gcal, '3100project', '2019-04-08', '18:00:00', '2019-04-08', '20:00:00')

    return redirect('portal-home')
