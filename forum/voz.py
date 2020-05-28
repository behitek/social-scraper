import datetime
import queue
import re
import traceback
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup

todo = queue.Queue()
found = set()
import os

HTTP_PROXY = "http://10.60.28.99:81"
# HTTP_PROXY = ""
os.environ['http_proxy'] = HTTP_PROXY
os.environ['https_proxy'] = HTTP_PROXY


def is_post(url):
    return re.match(r'https?://voz\.vn/t/.+', url) is not None


def correct_url(url):
    if url.startswith('javascript') or '/u/' in url or '/profile-posts/' in url:
        return ''
    if not url.startswith('http'):
        url = "https://voz.vn" + url
    url = re.sub('/?(unread|latest|#.+)/?$', '/', url)
    url = re.sub('/+$', '/', url)
    if re.match(r'https?://voz\.vn/.+', url):
        return url
    return ''


home_url = "https://voz.vn/"


def find_all_url(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        links = soup.find_all('a')
        for link in links:
            url = correct_url(link.get('href', ''))
            if url != '' and url not in found:
                found.add(url)
                todo.put(url)
    except:
        pass


def get_comment(url):
    comments = []
    r = requests.get(url)
    if r.status_code != 200:
        return 0
    soup = BeautifulSoup(r.content, 'lxml')
    for comment_html in soup.select('article.message-body.js-selectToQuote > div.bbWrapper'):
        try:
            for child in comment_html.select('blockquote'):
                child.extract()
        except:
            pass
        comment = comment_html.text.strip()
        if len(comment) > 0:
            comments.append(re.sub('\\n+', '\n', comment))
    with open('voz.txt', 'a+', encoding='utf8') as fp:
        for comment in comments:
            fp.write(comment + '\n---END_COMMENT---\n')
    return len(comments)


def worker(thread_name):
    while not todo.empty():
        url = todo.get()
        find_all_url(url)
        is_post_url = is_post(url)
        print(url, is_post_url)
        # TODO: Get comment
        if is_post_url:
            print('{} ; {} ; Found {} comments ; Todo = {} ; Found = {}'.format(datetime.datetime.now(), thread_name,
                                                                                get_comment(url), todo.qsize(),
                                                                                len(found)))


if __name__ == '__main__':
    find_all_url(home_url)
    print(datetime.datetime.now(), todo.qsize(), len(found))
    threads = []
    while todo.qsize() > 0:
        try:
            for i in range(10):
                t = Thread(target=worker, args=('Thread_{}'.format(i + 1),))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        except:
            traceback.print_exc()
            print('Sleep {} seconds.', 1000)
            sleep(1000)
