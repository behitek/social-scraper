import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://btv.org.vn/video/thoi-su-binh-duong/"
SAVE_DIR = "data/binhduongtv/thoisu.txt"
driver = webdriver.Firefox()

driver.get(URL)

all_hrefs = []

page = 0

while page <= 1120:
    sleep(2)
    hrefs = []
    for x in driver.find_elements_by_css_selector('div.image-wrapper > a'):
        x = x.get_attribute('href')
        if 'http' in x:
            hrefs.append(x)
    if len(hrefs) == 0:
        break
    all_hrefs.extend(hrefs)
    page += 20
    driver.get(URL + str(page))

for href in set(all_hrefs):
    try:
        driver.get(href)
        video_url = re.search('http://.+\\.mp4', str(driver.page_source)).group(0)
        print(video_url)
        with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
            fp.write(video_url + "\n")
    except:
        traceback.print_exc()

driver.close()
