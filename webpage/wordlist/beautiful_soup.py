import code
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://www.espn.com"
html = urlopen(url)

bsObj = BeautifulSoup(html.read(), features="lxml")
title = bsObj.find("meta",  property="og:title")
url = bsObj.find("meta",  property="og:url")

links = []

for link in bsObj.find_all('a'):
    links.append(link.get('href'))

print("Domain: " + url["content"] if url else "No meta url given")
print("Title: " + title["content"] if title else "No meta title given")
print("Links:")
for i in links:
    print(i)

