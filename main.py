import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'Wikipedia'
HOMEPAGE = 'https://www.wikipedia.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)

# create threads and tell them which work to do.
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# העבודה שהתהליכונים צריכים לעשות כאשר הם יופעלו
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# כל לינק שיש בתור מתחילים לסרוק אותו
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# התחלת הסריקה של הדפים, עוצר כאשר אין דפים לסרוק יותר
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

# start program
create_workers()
crawl()
