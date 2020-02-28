import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://www.ptpphuyen.vn/su-kien/thoi-su/?paged={}"
SAVE_DIR = "data/phuyentv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(1, 18):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_items = [x.get_attribute('href') for x in
                   driver.find_elements_by_css_selector('h3.title_tv > a')]
    for video_item in video_items:
        try:
            driver.get(video_item)
            script_tag = driver.find_element_by_css_selector('#content > div > div > script')
            video_url = "http://www.ptpphuyen.vn" + re.search("file: '(.+)',",
                                                              script_tag.get_attribute('innerHTML')).group(1)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()
driver.close()
