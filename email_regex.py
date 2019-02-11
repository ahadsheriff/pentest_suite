"""
Python script to scrape a web page for all email addresses
"""

from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
import re

url1 = "http://www.rit.edu/gccis/computingsecurity/people-categories/faculty"
url2 = "https://www.rit.edu/its/about/staff"

# a set of crawled emails
emails = set()

# get url's content
print("Processing %s" % url2)
response = requests.get(url2)

# extract all email addresses and add them into the resulting set

# regex for normally formatted emails. ex: ahadsheriff@gmail.com
email_normal = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
emails.update(email_normal)

# regex for emails formatted with a [dot]. ex: ahadsheriff@gmail[dot]com
email_dot = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\[dot\][A-Za-z]{2,4}", response.text, re.I))
emails.update(email_dot)

# regex for emails formatted with [at] and [dot]. ex: ahadsheriff[at]gmail[dot]com
email_at_dot = set(re.findall(r"[A-Za-z0-9._%+-]+\[at\][A-Za-z0-9.-]+\[dot\][A-Za-z]{2,4}", response.text, re.I))
emails.update(email_at_dot)


print(emails)
