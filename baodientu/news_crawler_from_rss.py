import requests
import feedparser
from newspaper import Article
import time
from collections import deque
import logging
import os, sys, re, json

proxy = "http://10.60.28.99:81"
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


rss_url = sys.argv[1]
output = sys.argv[2]

QUEUE_SIZE = 500
SLEEP = 10 * 60 # seconds


def crawl(url):
    article = Article(url)
    article.download()
    article.parse()
    result = {'url': url, 'error': '', 'success': True, 'title': article.title,
           'keywords': ', '.join(article.keywords if article.keywords else (
               article.meta_keywords if article.meta_keywords else article.meta_data.get('keywords', []))),
           'published_date': article.publish_date if article.publish_date
           else article.meta_data.get('pubdate', ''), 'top_img': article.top_image,
           'content': re.sub('\\n+', '</p><p>', '<p>' + article.text + '</p>')}
    return result

def get_rss(rss_url):
    urls = []
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        urls.append(entry['link'])
    return urls

found_set = set()
found_queue = deque()

def check_found(url):
    if url in found_set:
        return False
    if len(found_queue) == QUEUE_SIZE:
        q = found_queue.popleft()
        found_set.remove(q)
    found_queue.append(url)
    found_set.add(url)
    return True

if __name__ == '__main__':
    # print(crawl('https://vnexpress.net/hai-con-khi-dot-lay-nhiem-ncov-tu-nguoi-4219914.html'))
    start_time = time.time()
    while True:
        urls = get_rss(rss_url)
        for url in urls:
            if check_found(url):
                try:
                    data = crawl(url)
                    with open(output, 'a+') as fp:
                        fp.write(json.dumps(data, ensure_ascii=False) + '\n')
                    logger.info('Done {}'.format(url))
                except:
                	traceback.print_exc()
                    logger.error('Fail {}'.format(url))
        logger.info('Waiting {} s.'.format(SLEEP))
        time.sleep(SLEEP)


