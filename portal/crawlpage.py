#need to be added into view.py

# import bs4 lib
import re
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen


def crawlpage(url, crawltag):

	try:

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


		#change element to check valid? 
		#e.g. crawl error then return what>?

		return element

	except:

		s = sys.exc_info()
		print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
		
		error = re.search("\[.*\]", str(s[1]))
		print(error.group(0)[1:-1])

		return error.group(0)[1:-1]
