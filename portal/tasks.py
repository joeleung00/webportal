from random import randint
import datetime
import time

from . import crawlpage

def cron_update_grep_requests():
    time.sleep(randint(0, 30))
    crawlpage.process_grep_requests()
    print("[{}]Messages updated based on GrepRequests.".format(datetime.datetime.now()))

def sayhi():
    # For quick test on whether the cron job is really running
    print("hi")
