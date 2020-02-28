import traceback
from time import sleep

from selenium import webdriver

URL = "http://qbtv.vn/video.php?p=list_video&id=1"
SAVE_DIR = "data/qbtv/video.txt"
driver = webdriver.Firefox()


for i in range(4, 35):
    print('page =', i)
    driver.get(URL + "&page=" + str(i))
    video_eles = [x.get_attribute('href') for x in
                  driver.find_elements_by_css_selector('.media_box > a:nth-child(1)')]
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector(
                'video').get_attribute(
                'src')
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            traceback.print_exc()
driver.close()
