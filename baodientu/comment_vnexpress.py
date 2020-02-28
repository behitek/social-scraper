import json
import os
import re

import requests


class CommentCrawler:
    def __init__(self, post_url):
        self.post_url = post_url
        self.api_url = self.make_api_url()
        self.crawl()

    def make_api_url(self):
        r = requests.get(self.post_url)
        try:
            html = r.text
            self.objectid = re.sub('data-component-objectid="(\\d+)"', r'\1',
                                   re.findall('data-component-objectid="\\d+"', html)[0])
            siteid = re.sub('data-component-siteid="(\\d+)"', r'\1',
                            re.findall('data-component-siteid="\\d+"', html)[0])
            objecttype = re.sub('data-objecttype="(\\d+)"', r'\1',
                                re.findall('data-objecttype="\\d+"', html)[0])
            return "https://usi-saas.vnexpress.net/index/get?offset=0&limit=10000&frommobile=0&sort=like&is_onload=0&objectid={}&objecttype={}&siteid={}".format(
                self.objectid, objecttype, siteid)
        except:
            return None

    def crawl(self):
        if self.api_url is None:
            return []
        r = requests.get(self.api_url)
        if r.status_code != 200:
            return []
        json_comment = json.loads(r.content, encoding='utf8')

        comments = []
        if len(json_comment['data']) == 0:
            return
        for comment in json_comment['data']['items']:
            comments.append(comment['content'])
            if 'items' in comment['replys']:
                for item in comment['replys']['items']:
                    comments.append(item['content'])
        if len(comments) > 0:
            self.export(comments, self.objectid)

    def export(self, comments, objectid):
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('vnexpress_comment.txt', 'a+', encoding='utf8') as fp:
            for comment in comments:
                fp.write(comment + '\n\n')


if __name__ == '__main__':
    cm = CommentCrawler(
        'https://vnexpress.net/')
