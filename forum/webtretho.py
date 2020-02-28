import datetime
import queue
import re
import traceback
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup

todo = queue.Queue()
visited = set()


def is_post(url):
    return re.match(r'https?:\/\/(?:www\.)?webtretho\.com\/forum\/f\d+\/(?:\w+-)+\d+\/.*', url)


def correct_url(url):
    if url.startswith('/'):
        url = "https://webtretho.com" + url
    if is_post(url):
        return re.sub(r'(https?:\/\/(?:www\.)?webtretho\.com\/forum\/f\d+\/(?:\w+-)+\d+\/?).+', r'\1/', url)
    elif re.match('https?://webtretho.+', url):
        return url
    return ''


home_url = "https://www.webtretho.com/"


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


def get_comment(url):
    comments = []
    page = 1
    while True:
        _url = url if page == 1 else url + 'index{}.html'.format(page)
        r = requests.get(_url)
        if r.status_code != 200 or r.url != _url:
            break
        soup = BeautifulSoup(r.content, 'lxml')
        for comment_html in soup.select('blockquote.postcontent.restore'):
            try:
                comment_html.find('div', class_='bbcode_container').decompose()
            except:
                pass
            comment = comment_html.text.strip()
            if len(comment) > 0:
                comments.append(comment)
        page += 1
    with open('webtretho.txt', 'a+', encoding='utf8') as fp:
        for comment in comments:
            fp.write(comment + '\n\n')


def worker(thread_name):
    while not todo.empty():
        url = todo.get()
        find_all_url(url)
        # TODO: Get comment
        print(url)
        get_comment(url)
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
    # get_comment('https://www.webtretho.com/forum/f4729/6-bieu-hien-tre-thong-minh-vo-cung-ma-khong-phai-bo-me-nao-cung-nhan-ra-2760644')
    # print('Done!')
