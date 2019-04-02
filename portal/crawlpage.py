#need to be added into view.py

# import bs4 lib
from bs4 import BeautifulSoup
from urllib.request import urlopen


def crawlpage(url, crawltag):
	#logic for crawling
	html = urlopen(url).read().decode('utf-8')
	soup = BeautifulSoup(html ,'html.parser')
	element = soup.select(crawltag)

	# hardcode version:
	# html = urlopen("http://course.cse.cuhk.edu.hk/~csci3100/").read().decode('utf-8')
	# soup = BeautifulSoup(html ,'html.parser')
	# print_text = soup.select('br+ p')
	# print(print_text)

	#crawl result is return as a list

	return element
