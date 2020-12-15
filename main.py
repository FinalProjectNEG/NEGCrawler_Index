from collections import deque

import requests
import re
from urllib.parse import urlparse
import os

from DB import insertDB, Insert_Graph
from Link_finder import LinkFinder
from Setting import init


from bs4 import BeautifulSoup


graph_links = {}

class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = []
        self.queue = deque([])
        self.proxy_orbit_key = os.getenv("PROXY_ORBIT_TOKEN")
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        self.proxy_orbit_url = f"https://api.proxyorbit.com/v1/?token={self.proxy_orbit_key}&ssl=true&rtt=0.3&protocols=http&lastChecked=30"

    def get_html(self, url):

        try:
            html = requests.get(url, headers={"User-Agent":self.user_agent}, timeout=10)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('utf-8')

    def get_links(self, url):

        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):

            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url):
        html = self.get_html(url)
        meta = re.findall("<meta .*?[name,content]=[\"'](.*?)['\"].*?[content,name]=[\"'](.*?)['\"].*?>", html)
        soup = BeautifulSoup(html, 'html.parser')
        if soup.find('title'):
            title = soup.find('title').text
        else:
            title=""
        return dict(meta), title,html

    def crawl(self, url):
        self.visited.append(url)
        if len(self.queue) > 1:
            return
        links = self.get_links(url)
        graph_links[url] = links
        for link in links:
            flag = 0

            for element in self.queue:
                if element == link:
                    flag = 1
                    break

            if flag == 0:
                if len(self.queue) > 1:
                    return
                if link in self.visited:
                    continue
                if (self.visited.count(link)) == 0:
                    self.queue.append(link)
            # if link in self.visited:
            #     continue

            info, title, html = self.extract_info(link)
            object = LinkFinder(url,info, title, html)

            print(f"""Link: {link}    
Description: {info.get('description')}    
Keywords: {info.get('keywords')}
            """)
        current = self.queue.popleft()
        self.crawl(current)

    def start(self):
        info, title, html = self.extract_info(self.starting_url)
        object = LinkFinder(self.starting_url, info, title, html)
        print("start crawling!")
        self.crawl(self.starting_url)
        insertDB()
        Insert_Graph(graph_links)


if __name__ == "__main__":

    init()
    crawler = PyCrawler("https://www.google.com/")
    crawler.start()