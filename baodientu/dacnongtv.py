import re
import traceback

from selenium import webdriver

url = "http://truyenhinhdaknong.vn/video/thoi-su-dak-nong/2000"
SAVE_DIR = "data/dacnongtv/thoi-su.txt"
driver = webdriver.Firefox()

stt = 2020

while url:
    print(url)
    driver.get(url)
    video_eles = set()
    for x in driver.find_elements_by_css_selector('div.tv-col-left-video a.image'):
        video_eles.add(x.get_attribute('href'))

    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector(
                '#site-body > div > div.b-listing-content.clearfix > div.block-player > script').get_attribute(
                'innerHTML')
            video_url = re.search(r'link_play_livestream = \"(http:.+)\";', video_url).group(1)
            # try:
            #     video_url = re.search(r"file=(http.+\..+)&image=", video_url).group(1)
            # except:
            #     video_url = driver.find_element_by_css_selector('embed#media').get_attribute('src')
            print(video_url, driver.title)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                if not video_url.endswith('.mp3'):
                    fp.write(video_url + "\n")
        except:
            print(video_ele)
            traceback.print_exc()

    if stt == 2760:
        break
    url = "http://truyenhinhdaknong.vn/video/thoi-su-dak-nong/{}".format(stt)
    stt += 20
    # print(stt)

driver.close()
