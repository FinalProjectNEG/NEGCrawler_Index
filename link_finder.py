import os
import re
from html.parser import HTMLParser
from urllib import request

import DB

import requests
from bs4 import BeautifulSoup
from Index import Index

class LinkFinder():

    def __init__(self, urlPage,info,title, html, time):

        self.base_url = urlPage
        self.html = html
        self.title = title
        self.text = ""
        self.dictionary = info
        self.time = time
        self.Description()


    def Description(self):

        #data = self.html.read().decode('utf-8')

        # display html format to easy to navigate and to parse the html tags
        soup = BeautifulSoup(self.html, 'html.parser')

        # kill all script and style elements
        for script in soup(["script", "style", '[document]', 'head']):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        self.text = '\n'.join(chunk for chunk in chunks if chunk)
        print(self.text)
        if self.dictionary.get('description')==None or len(self.dictionary.get('description').split(sep=" "))<5:
            temp = text.split(sep=" ")[:20]
            self.dictionary['description'] = '\n'.join(chunk for chunk in temp if chunk)
            print(self.dictionary['description'])
        Create_index = Index(self.text, self.base_url,self.title, self.dictionary.get('description'), self.time)
        Create_index.calculate_score()

        #print(text)
