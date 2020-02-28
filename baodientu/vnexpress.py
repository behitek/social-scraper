import datetime
import queue
import re
import traceback
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup

from comment_crawler import CommentCrawler

todo = queue.Queue()
visited = set()


def is_post(url):
    return re.match(r'https:\/\/vnexpress\.net\/(?:\w+-)?\w+\/(?:\w+-)+\w+\.html.*', url)


def correct_url(url):
    if is_post(url):
        return re.sub(r'(https:\/\/vnexpress\.net\/(?:\w+-)?\w+\/(?:\w+-)+\w+\.html).*', r'\1', url)
    elif re.match('https://vnexpress.+', url):
        return url
    return ''


home_url = "https://vnexpress.net/"


def find_all_url(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        links = soup.find_all('a')
        for link in links:
            url = correct_url(link.get('href', ''))
            if url != '' and url not in visited:
                visited.add(url)
                todo.put(url)
    except:
        pass


def worker(thread_name):
    while not todo.empty():
        url = todo.get()
        find_all_url(url)
        CommentCrawler(url)
        print(datetime.datetime.now(), thread_name, todo.qsize(), len(visited))


if __name__ == '__main__':
    find_all_url(home_url)
    print(datetime.datetime.now(), todo.qsize(), len(visited))
    threads = []
    while todo.qsize() > 0:
        try:
            for i in range(5):
                t = Thread(target=worker, args=('Thread_{}'.format(i + 1),))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        except:
            traceback.print_exc()
            print('Sleep {} seconds.', 1000)
            sleep(1000)



print('Done!')
