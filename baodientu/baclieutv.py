import re
import traceback

from selenium import webdriver

URL = "http://thbl.vn/?cat=39&paged={}"
SAVE_DIR = "data/baclieutv/nhanai.txt"
driver = webdriver.Firefox()

for i in range(1, 16):
    print('page =', i)
    driver.get(URL.format(i))
    videos = []

    for x in driver.find_elements_by_css_selector('div.post-thumbnail > a'):
        videos.append(x.get_attribute('href'))

    for video in videos:
        try:
            driver.get(video)
            # if not driver.title.lower().startswith('thời sự'):
            #     continue
            video_url = driver.find_element_by_css_selector('iframe').get_attribute('src')
            video_url = re.search(r'l=(http.+\.mp4)&i=', video_url).group(1)
            print(video_url)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()
driver.close()
