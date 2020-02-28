import traceback
from time import sleep

from selenium import webdriver

URL = "http://truyenhinhdulich.vn/video/van-de-va-binh-luan?page={}"
SAVE_DIR = "data/van-de-va-binh-luan.txt"
driver = webdriver.Firefox()

print(SAVE_DIR)

mp3_urls = set()

for i in range(1, 6):
    print('page =', i)
    driver.get(URL.format(str(i)))
    video_eles = []
    for x in driver.find_elements_by_css_selector('h3 > a.block-title'):
        if '/video/' in x.get_attribute('href'):
            video_eles.append(x.get_attribute('href'))
    for x in driver.find_elements_by_css_selector('h5.blog-title > a'):
        if '/video/' in x.get_attribute('href'):
            video_eles.append(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('div#video_player').get_attribute(
                'data-src')
            print(video_url)
            if video_url not in mp3_urls:
                with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                    fp.write('http://truyenhinhdulich.vn' + video_url + "\n")
                mp3_urls.add(video_url)
        except:
            traceback.print_exc()

driver.close()
