from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domaim_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domaim_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # create directory of the name project like "Wikipedia" and create the files "queue.txt", "crawler.txt"
    @staticmethod
    def boot():
        # create directory with the name project
        create_project_directory(Spider.project_name)
        # create the files
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    #
    @staticmethod
    def crawl_page(thread_name, page_url):
        # אם לא זחלנו בו בעבר אז...
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling '+page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled '+ str(len(Spider.crawled)))
            # insert the page_url to the queue and do crawl bi function:"gather_links"
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            # finish to crawl the page and remove him from the queue
            Spider.queue.remove(page_url)
            # add the page_url to list "crawled"
            Spider.crawled.add(page_url)
            # update the files with the correct information
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            # open the url
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=utf-8':
                # read the html text (return text in bytes)
                html_bytes = response.read()
                # turn the bytes text to english text by "utf-8"
                html_string = html_bytes.decode("utf-8")
            # create LinkerFinder object to parse the html text and take from there the links in the page and save in database
            finder = LinkFinder(Spider.base_url, page_url)
            # Feed some text to the parser. It is processed insofar as it consists of complete elements.
            finder.feed(html_string)
        except Exception as exc:
            print('Error: can not crawl page'+ " "+ str(exc))
            return set()

        return finder.page_links()

    # add link to the queue
    @staticmethod
    def add_links_to_queue(links):
        for url in links:

            # אם הוא נמצא כבר
            if url in Spider.queue:
                continue
            # אם כבר סרקנו את הקישור כבר בעבר
            if url in Spider.crawled:
                continue
            # אם הלינק הוא לא בעל שם הדומיין שאנחנו בו
            if Spider.domaim_name not in url:
                continue
            Spider.queue.add(url)

    # function to set the files "queue.txt" and "crawler.txt"
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)






