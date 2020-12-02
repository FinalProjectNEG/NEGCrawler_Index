import urllib
from html.parser import HTMLParser
from urllib import parse
import re

from nltk import WordPunctTokenizer

from ReinforcementLearning import ReinforrcementLearning
from bs4 import BeautifulSoup
import DB
import requests


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        HTMLParser.__init__(self)
        self.base_url = base_url
        self.page_url = page_url
        # take the description and title of the page
        self.description_page(self.page_url)
        # insert to database the information of the page
        DB.insertDB(self.page_url, self.title)
        self.links = set()

    # overrides, find the links in the page for the crawler
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass


    #הוצאת מידע אודות הדף אינטרנט: title description
    def description_page(self, url):
        # open the url by request
        response11 = requests.get(url)

        data = response11.text

        # display html format to easy to navigate and to parse the html tags
        soup = BeautifulSoup(data, 'html.parser')

        self.title = ""
        if soup.title:
            self.title = soup.title.string
            print(self.title)


        self.text_decription = soup.find('meta', {'name':'description'}).text
        # kill all script and style elements
        for script in soup(["script", "style",'[document]', 'head', 'title']):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        obj = ReinforrcementLearning(text)
        maximize = obj.calculate_score(text)
        print(maximize)