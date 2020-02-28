import re
import traceback

from selenium import webdriver

URL = "http://www.thtg.vn/videos/ban-tin-thoi-su-toi/page/{}"
SAVE_DIR = "data/tiengiangtv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(91, 165):
    print('page =', i)
    driver.get(URL.format(i))
    videos = []

    for x in driver.find_elements_by_css_selector('h2.title > a'):
        videos.append(x.get_attribute('href'))

    for video in videos:
        try:
            driver.get(video)
            # if not driver.title.lower().startswith('thời sự'):
            #     continue
            video_url = driver.find_element_by_css_selector('#download-video').get_attribute('href')
            print(video_url)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()
driver.close()
