import re
import traceback

import requests
from bs4 import BeautifulSoup

HOME_URL = "http://ntucoder.net/Message"

comments = set()

url = HOME_URL

page = 1
while True:
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        for comment in soup.select('div.message-info > div'):
            txt = re.sub('^[^:]+:', '', comment.text.strip()).strip()
            if txt != '':
                comments.add(txt)
        url = "http://ntucoder.net{}".format(soup.select_one('#view-previous-con > a')['href'])
        page+= 1
    except:
        traceback.print_exc()
        break

print("Total pages = {}".format(page))

with open('ntucoder.txt', 'w', encoding='utf8') as fp:
    for x in comments:
        fp.write(x + '\n\n')
