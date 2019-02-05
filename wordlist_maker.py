"""
Create a word-list from a given website using BeautifulSoup.
Gets all body text from a webpage and adds all unique words to a set.
Ignoress all style, script, head, and title tags.
"""

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request    
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque


def tags(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_body(body):

    word_list = set()

    soup = BeautifulSoup(body, 'html.parser')
    get_body = soup.findAll(text=True)
    visible_texts = filter(tags, get_body) 

    text = u" ".join(t.strip() for t in visible_texts)

    get_words = set(text.split())
    word_list.update(get_words)

    print(word_list)

def crawler(url, body):
    # a queue of urls to be crawled
    new_urls = deque([url])

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    word_list = set()

    # process urls one by one until we exhaust the queue
    while len(new_urls):

        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # get url's content
        print("Processing %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        soup = BeautifulSoup(body, 'html.parser')
        get_body = soup.findAll(text=True)
        visible_texts = filter(tags, get_body) 

        text = u" ".join(t.strip() for t in visible_texts)

        get_words = set(text.split())
        word_list.update(get_words)

        print(word_list)

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text)

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in new_urls and not link in processed_urls:
                new_urls.append(link)

if __name__ == "__main__":
    print("PROCESSING WEBPAGE...")

    url = 'http://www.espn.com/nfl/story/_/id/25921740/super-bowl-liii-was-greatest-defensive-performance-history-here-how-patriots-did-rams'
    body = urllib.request.urlopen(url).read()
    print(get_body(body))

    print()
    print("CRAWLING WEBSITE...")
    #crawler(url,body)

