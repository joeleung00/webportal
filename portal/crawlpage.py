#need to be added into view.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Message
from django.contrib.auth.models import User
from django.views.decorators import csrf

# import bs4 lib
from bs4 import BeautifulSoup
from urllib.request import urlopen


def crawlpage(request):
	content = {}
	if request.user.is_authenticated:
		if "crawllink" in request.POST:
			print(request.POST["crawllink"])
			#logic for crawling
			#html = urlopen({{crawllink}}).read().decode('utf-8')
			#soup = BeautifulSoup(html ,'html.parser')
			#element = soup.select({{crawltag}})

	# hardcode version:
	# html = urlopen("http://course.cse.cuhk.edu.hk/~csci3100/").read().decode('utf-8')
	# soup = BeautifulSoup(html ,'html.parser')
	# print_text = soup.select('br+ p')
	# print(print_text)

	#crawl result is return as a list

	return render(request, 'portal/crawlpage.html')
