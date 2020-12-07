import re
from html.parser import HTMLParser
import DB

import requests
from bs4 import BeautifulSoup


class LinkFinder():

    def __init__(self, urlPage,info):

        self.base_url = urlPage
        self.html = requests.get(self.base_url)
        self.title=""
        self.text=""
        self.dictionary = info
        self.Description()
        DB.insertDB(urlPage,self.title,self.dictionary.get('description'))


    def Description(self):

        data = self.html.text

        # display html format to easy to navigate and to parse the html tags
        soup = BeautifulSoup(data, 'html.parser')

        if soup.title:
            self.title = soup.title.string

        # kill all script and style elements
        for script in soup(["script", "style", '[document]', 'head', 'title']):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        self.text = '\n'.join(chunk for chunk in chunks if chunk)
        #print(text)
