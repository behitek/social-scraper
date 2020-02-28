import os
import re
from datetime import datetime, timedelta
from random import choice

import requests
from bs4 import BeautifulSoup
from news_prep import news_prep
from newspaper import Article

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def to_string(date):
    return date.strftime("%d-%m-%Y")


def to_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y")


class VnExpress:
    def __init__(self, start_date, end_date, export_dir):
        self.url = "https://thethao.tuoitre.vn/the-thao/xem-theo-ngay/{}.htm"
        self.start_date = to_date(start_date)
        self.end_date = to_date(end_date)

        self.export_dir = export_dir
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
        self.output = os.path.join(self.export_dir,
                                   "tuoitre_" + re.sub(r"/", ".", start_date) + "-" + re.sub(r"/", ".", end_date))
        if os.path.exists(self.output):
            os.remove(self.output)

    def add_days(self, num_of_days=1):
        self.start_date += timedelta(days=num_of_days)

    def crawl_able(self):
        return self.start_date <= self.end_date

    def crawl(self):
        while self.crawl_able():
            date_str = to_string(self.start_date)
            print('DATE', date_str)
            res = requests.get(self.url.format(date_str), headers=random_headers())
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'lxml')
                news_articles = soup.select('h3.title-news > a')
                for news_article in news_articles:
                    # time.sleep(randint(1, 5))
                    url = "https://thethao.tuoitre.vn" + news_article['href']
                    print(url, self.get_content(url))
            self.add_days(num_of_days=1)

    def get_content(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            content = ''
            if article.title:
                content += article.title + "\n"
            # if article.meta_description:
            #     content += article.meta_description + "\n"
            if article.text and len(article.text) > 50:
                content += article.text

            content = news_prep(content)
            if content:
                with open(self.output, 'a+', encoding='utf8') as fp:
                    fp.write(content + "\n")
                    fp.write("\n")
                return "SUCCESS!"
            else:
                return "EMPTY!"
        except:
            return "FAILURE!"


if __name__ == '__main__':
    vnexpress = VnExpress('01/01/2004', '31/05/2019', '../data/tuoitre_thethao')
    vnexpress.crawl()
