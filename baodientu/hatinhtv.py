import traceback
from time import sleep

from selenium import webdriver


def thoisu():
    URL = "http://hatinhtv.vn/thoi-su"
    SAVE_DIR = "data/hatinhtv/thoi-su.txt"
    driver = webdriver.Firefox()

    for i in range(16, 28):
        print('page =', i)
        driver.get(URL + "?page=" + str(i))
        video_eles = [x.get_attribute('href') for x in driver.find_elements_by_css_selector('a.image.mb-15')]
        for video_ele in video_eles:
            try:
                driver.get(video_ele)
                sleep(2)
                video_url = driver.find_element_by_css_selector(
                    '#main-wrapper > div.container.nen-trang > div > div > div.col-lg-8.col-12.box-mobile > '
                    'div.single-blog.mb-15 > div > div.post-video > div.video-container.responsive-video > video > '
                    'source').get_attribute(
                    'src')
                with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
                    fp.write(video_url + "\n")
            except:
                traceback.print_exc()
    driver.close()


def daibieuvoicutri():
    URL = "http://hatinhtv.vn/vi/dai-bieu-dan-cu-voi-cu-tri"
    SAVE_DIR = "data/hatinhtv/dai-bieu-dan-cu-voi-cu-tri.txt"
    driver = webdriver.Firefox()

    with open(SAVE_DIR, 'w', encoding='utf8') as fp:
        for i in range(1, 2):
            driver.get(URL + "?page=" + str(i))
            video_eles = [x.get_attribute('href') for x in driver.find_elements_by_css_selector('a.image.mb-15')]
            for video_ele in video_eles:
                driver.get(video_ele)
                video_url = driver.find_element_by_css_selector(
                    '#main-wrapper > div.container.nen-trang > div > div > div.col-lg-8.col-12.box-mobile > '
                    'div.single-blog.mb-15 > div > div.post-video > div.video-container.responsive-video > video > '
                    'source').get_attribute(
                    'src')
                fp.write(video_url + "\n")
    driver.close()


if __name__ == '__main__':
    thoisu()
