#need to be added into view.py

# import bs4 lib
from bs4 import BeautifulSoup
from urllib.request import urlopen

from .netgrep.parsehtml import ParseHtml
from . import models as db

def process_oneoff_grep_request(url, xpath_pattern):
	#
    # Directly update the target message on trigger
	#

    # Parse and get target content
    target_xpath = xpath_pattern
    target_content = ""
    multiple = ParseHtml.retrieve_xpath_matches(target_xpath, url)
    for elem in multiple:
        target_content += ParseHtml.convert_lxml_element_to_string(elem, truncate=80) + '\n'
    if target_content == "":
        target_content = "Target not found, please consider refreshing your request."

    return target_content

def process_grep_requests():
	#
    # Currently just directly update the target message on trigger
    # TODO: add grep_requests to queue and process them sequentially in background process
	#

	grep_requests = db.GrepRequest.objects.all()
	for request in grep_requests:
		# Parse and get target content
		target_content = process_oneoff_grep_request(request.url, request.crawltag)

		# Find corresponding message to update
		message = request.message
		message.content = target_content
		message.save()

def crawlpage(url, crawltag):
	#logic for crawling
	return process_oneoff_grep_request(url, crawltag)
