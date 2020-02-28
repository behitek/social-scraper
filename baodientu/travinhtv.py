import re
import time
import traceback

from selenium import webdriver

URL = "http://travinhtv.vn/thtv/media/cmeptv/AV/{}/17"
SAVE_DIR = "data/travinhtv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(8, 77):
    print('page =', i)
    driver.get(URL.format(i))
    videos = []

    for x in driver.find_elements_by_css_selector('div#title > a'):
        videos.append(x.get_attribute('href'))

    for video in videos:
        try:
            time.sleep(1)
            driver.get(video)
            # if not driver.title.lower().startswith('thời sự'):
            #     continue
            video_url = driver.find_element_by_css_selector('video > source').get_attribute('src')
            print(video_url)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            print('error:', video)
            traceback.print_exc()
driver.close()
