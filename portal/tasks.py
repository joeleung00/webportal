from random import randint
import datetime
import time

from .netgrep.parsehtml import ParseHtml
from . import models as db

def process_grep_requests():
    # Currently just directly update the target message on trigger
    # TODO: add grep_requests to queue and process them sequentially in background process
    grep_requests = db.GrepRequest.objects.all()
    for request in grep_requests:
        # Parse and get target content
        target_xpath = request.selected_content
        target_content = ""
        multiple = ParseHtml.retrieve_xpath_matches(target_xpath, request.url)
        for elem in multiple:
            target_content += ParseHtml.convert_lxml_element_to_string(elem, truncate=80) + '\n'
        if target_content == "":
            target_content = "Target not found, please consider refreshing your request."

        # Find corresponding message to update
        message = request.message
        message.content = target_content
        message.save()

def cron_update_grep_requests():
    time.sleep(randint(0, 30))
    process_grep_requests()
    print("[{}]Messages updated based on GrepRequests.".format(datetime.datetime.now()))

def sayhi():
    # For quick test on whether the cron job is really running
    print("hi")
