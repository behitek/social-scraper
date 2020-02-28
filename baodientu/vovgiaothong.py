import re
import traceback
from time import sleep
import urllib.parse
from selenium import webdriver
from selenium.webdriver import ActionChains

URL = "http://vovgiaothong.vn/Article/ViewList.aspx?pageid=679&mid=1637&pagenumber={}"
SAVE_DIR = "data/vovgiaothong/dien-dan.txt"
driver = webdriver.Firefox()

print(SAVE_DIR)

mp3_urls = set()

for i in range(1, 9):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('.article-title > a'):
        video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('iframe').get_attribute(
                'src')
            video_url = urllib.parse.unquote(re.sub('.+href=(.+)&show_text.+', r'\1', video_url))
            # print(video_url)
            if video_url not in mp3_urls:
                with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                    fp.write(video_url + "\n")
                mp3_urls.add(video_url)
        except:
            traceback.print_exc()

driver.close()
