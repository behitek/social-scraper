import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://quangngaitv.vn/tin-tuc-c202/thoi-su.html?trang={}"
SAVE_DIR = "data/quangngaitv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(1, 71):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('.mnv-title-news > a'):
        if 'thời sự' in x.text.lower():
            video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('#stream').get_attribute('src')
            driver.get(video_url)
            while True:
                try:
                    driver.find_element_by_css_selector('#embed-player_display_button').click()
                    break
                except:
                    sleep(1)
            video_url = driver.find_element_by_css_selector('#embed-player_media > video').get_attribute('src')
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()

driver.close()
