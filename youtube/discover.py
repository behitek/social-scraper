import datetime
import os
import re
import time
import traceback
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup

try:
    from youtube.downloader import download
except:
    from downloader import download

LOGTYPE = {
    "INFO": "INFO",
    "ERROR": "ERROR"
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'


def generate_filename(data_dir):
    return os.path.join(data_dir, 'youtube_{}.txt'.format(datetime.datetime.today().strftime('%Y%m%d')))


def log(mes, log_type=LOGTYPE["INFO"]):
    print(log_type, datetime.datetime.now(), mes)


def is_vietnam_video(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    r = session.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            title = soup.find("meta", property="og:title")['content'].lower()
        except:
            return False
        # print(title)
        return len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', title)) > 3
    elif r.status_code == 429:
        print('Got', url, r.status_code)
        time.sleep(1)
        return is_vietnam_video(url)
    else:
        return False


class Discover:
    def __init__(self, init_url=[], data_dir=''):
        self.discover_id = Queue()
        self.visited_id = set()
        self.data_dir = data_dir
        for url in init_url:
            self.discover_id.put(url)

    def grab_url(self, input_url, thread_name):
        try:
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            r = session.get(input_url)
            if r.status_code == 200:
                urls = re.findall(r'/watch\?v=.{11}"', r.text)
                count = 0
                for url in urls:
                    url = re.sub(r'/watch\?v=(.{11})"', r"\1", url)
                    if url not in self.visited_id and is_vietnam_video('https://youtube.com/watch?v={}'.format(url)):
                        count += 1
                        self.discover_id.put(url)
                        self.visited_id.add(url)
                log('{} - {}: Found {} new urls.'.format(thread_name, input_url, count) + ' discover_size: {}'.format(
                    self.discover_id.qsize()))
            elif r.status_code == 429:
                print('Got', input_url, r.status_code)
                time.sleep(1)
                self.grab_url(input_url)
        except:
            log(traceback.format_exc(), LOGTYPE['ERROR'])

    def worker(self, thread_name):
        while not self.discover_id.empty():
            try:
                url = self.discover_id.get()
                self.grab_url(url if url.startswith('http') else 'https://youtube.com/watch?v={}'.format(url), thread_name)
                if len(url) == 11:
                    count = download(url, "data/" + thread_name + "_youtube.txt", 0, True)
                    log('{} - Download {}: {} comment(s).'.format(thread_name, url, count))
            except:
                log(traceback.format_exc(), LOGTYPE['ERROR'])

    def start(self, num_thread=5):
        threads = []
        for i in range(num_thread):
            t = Thread(target=self.worker, args=('thread_{}'.format(i + 1),))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
