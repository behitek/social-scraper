import re
import traceback
from time import sleep

from selenium import webdriver

URL = "http://quangtritv.vn/video-v18053/c1/thoi-su.html?trang={}"
SAVE_DIR = "data/quangtritv/thoisu.txt"
driver = webdriver.Firefox()

for i in range(159, 166):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('a.tlm-video-box-title'):
        if 'thời sự' in x.text.lower():
            video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            video_ele = re.sub(r".+/video-v(\d+)/.+", r"\1", video_ele)
            driver.get("http://quangtritv.vn/Modules/video/PlayVideo.aspx?videoId={}".format(video_ele))
            while True:
                try:
                    driver.find_element_by_css_selector('#embed-player_display_button').click()
                    break
                except:
                    sleep(1)
            try:
                video_url = driver.find_element_by_css_selector(
                    '#embed-player_media > video').get_attribute(
                    'src')
                with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                    fp.write(video_url + "\n")
            except:
                video_url = driver.find_element_by_css_selector(
                    '#embed-player_youtube').get_attribute(
                    'src')
                with open(SAVE_DIR + ".youtube", 'a+', encoding='utf8') as fp:
                    fp.write(
                        "https://www.youtube.com/watch?v={}".format(re.sub(r".+embed/(.+)\?autoplay.+", r"\1", video_url)) + "\n")
                print('Detected video youtube src!!!')
        except:
            traceback.print_exc()

driver.close()
