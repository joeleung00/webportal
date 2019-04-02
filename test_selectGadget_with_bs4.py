#testing bs4

from bs4 import BeautifulSoup
from urllib.request import urlopen

# remember to use CUHK network
html = urlopen("http://course.cse.cuhk.edu.hk/~csci3100/").read().decode('utf-8')

soup = BeautifulSoup(html ,'html.parser')


print_text = soup.select('br+ p') #return list
print(print_text)


with open('crawlData.txt', 'w') as text_file:
    for element in print_text:
        text_file.write("%s\n" % element)

    print("")
    print("finish writing text_file")

text_file.close()