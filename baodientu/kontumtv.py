import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://kontumtv.vn/category/video-clip/thoi-su/page/{}"
SAVE_DIR = "data/kontumtv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(60, 265):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('.post-thumb > a'):
        video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('center > iframe').get_attribute(
                'src')
            video_url = re.search(r"\?l=(http.+\.mp4)", video_url).group(1)
            print(video_url)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()

driver.close()
