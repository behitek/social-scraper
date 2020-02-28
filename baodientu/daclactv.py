import re
import traceback

from selenium import webdriver

url = "https://drt.org.vn/component/video/?itemid=&task=99"
SAVE_DIR = "data/daclactv/trang_dia_phuong.txt"
driver = webdriver.Firefox()

stt = 21

while url:
    # print(url)
    driver.get(url)
    video_eles = set()
    for x in driver.find_elements_by_css_selector('a.truyenhinh'):
        video_eles.add(x.get_attribute('href'))
    for video_ele in video_eles:
        try:
            driver.get(video_ele)
            video_url = driver.find_element_by_css_selector('#myId > object > param:nth-child(8)').get_attribute(
                'value')
            try:
                video_url = re.search(r"file=(http.+\..+)&image=", video_url).group(1)
            except:
                video_url = driver.find_element_by_css_selector('embed#media').get_attribute('src')
            # print(video_url)
            with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                fp.write(video_url + "\n")
        except:
            print(video_ele)
            traceback.print_exc()

    if stt == 168:
        break
    url = "https://drt.org.vn/index.php?task=99&option=com_video&amount=21&st={}".format(stt)
    stt += 21
    print(stt)

driver.close()
