import datetime
import os
import re
import traceback
from queue import Queue

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


def generate_filename(data_dir):
    return os.path.join(data_dir, 'youtube_{}.txt'.format(datetime.datetime.today().strftime('%Y%m%d')))


def log(mes, log_type=LOGTYPE["INFO"]):
    print(log_type, datetime.datetime.now(), mes)


def is_vietnam_video(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.title.string.lower()
        return len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', title)) > 3
    else:
        return False


class Discover:
    def __init__(self, init_url=[], data_dir=''):
        self.discover_id = Queue()
        self.visited_id = set()
        self.data_dir = data_dir
        for url in init_url:
            self.discover_id.put(url)

    def grab_url(self, input_url):
        try:
            r = requests.get(input_url)
            if r.status_code == 200:
                urls = re.findall(r'/watch\?v=.{11}"', r.text)
                count = 0
                for url in urls:
                    url = re.sub(r'/watch\?v=(.{11})"', r"\1", url)
                    if url not in self.visited_id and is_vietnam_video('https://youtube.com/watch?v={}'.format(url)):
                        count += 1
                        self.discover_id.put(url)
                        self.visited_id.add(url)
                log('{}: Found {} new urls.'.format(input_url, count) + ' discover_size: {}'.format(
                    self.discover_id.qsize()))
        except:
            log(traceback.format_exc(), LOGTYPE['ERROR'])

    def start(self):
        while not self.discover_id.empty():
            try:
                url = self.discover_id.get()
                self.grab_url(url if url.startswith('http') else 'https://youtube.com/watch?v={}'.format(url))
                if len(url) == 11:
                    count = download(url, generate_filename(self.data_dir), 0, True)
                    log('Download {}: {} comment(s).'.format(url, count))
            except:
                log(traceback.format_exc(), LOGTYPE['ERROR'])
