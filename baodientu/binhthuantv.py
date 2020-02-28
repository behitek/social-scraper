import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://binhthuantv.vn/loai-videos/thoi-su-sang-42.html"
SAVE_DIR = "data/binhthuantv/thoisu.txt"
driver = webdriver.Firefox()

driver.get(URL)

all_hrefs = []

for i in range(34):
    sleep(2)
    hrefs = []
    content_div = driver.find_element_by_css_selector('#ctl00_SC_Main_UpdatePanel2')
    for x in content_div.find_elements_by_tag_name('a'):
        x = x.get_attribute('href')
        if 'http' in x:
            hrefs.append(x)
    if len(hrefs) == 0:
        break
    all_hrefs.extend(hrefs)
    driver.find_element_by_css_selector('#ctl00_SC_Main_rptPager_ctl05_lnkPage').click()

for href in set(all_hrefs):
    try:
        driver.get(href)
        try:
            video_url = driver.find_element_by_css_selector('#stream_video_youtube').get_attribute('src')
            video_url = "https://www.youtube.com/watch?v={}".format(
                re.search(r"youtube.com/embed/(.+)\?", video_url).group(1))
            with open(SAVE_DIR + ".youtube", 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            video_url = driver.find_element_by_css_selector(
                '#stream_video > div.jw-media.jw-reset > video').get_attribute('src')
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
    except:
        traceback.print_exc()

driver.close()
