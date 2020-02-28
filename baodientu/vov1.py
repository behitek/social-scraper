import traceback
from time import sleep

from selenium import webdriver

URL = "http://vov1.vn/360-do-suc-khoe-c139-p{}.aspx"
SAVE_DIR = "data/vov1/360-do-suc-khoe.txt"
driver = webdriver.Firefox()

print(SAVE_DIR)

mp3_urls = set()

for i in range(1, 9):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('.title > a'):
        video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('static > source').get_attribute(
                'src')
            # print(video_url)
            if video_url not in mp3_urls:
                with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                    fp.write(video_url + "\n")
                mp3_urls.add(video_url)
        except:
            traceback.print_exc()

driver.close()
