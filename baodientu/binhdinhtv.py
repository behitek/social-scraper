import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://www.binhdinhtv.vn/tvcategory.ita?cid=1"
SAVE_DIR = "data/binhdinhtv/thoisu.txt"
driver = webdriver.Firefox()

driver.get(URL)

for video in driver.find_elements_by_css_selector('td.bantin > a'):
    video_url = re.sub(r"play\('(.+)',.+", r'\1', video.get_attribute('onclick'))
    with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
        fp.write(video_url + "\n")

driver.close()
