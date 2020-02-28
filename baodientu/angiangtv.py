from selenium import webdriver

URL = "http://atv.org.vn/video/thoi-su-45.html?page={}"
MAX_PAGE = 94
SAVE_DIR = "data/angiangtv/thoisu.txt"
driver = webdriver.Firefox()

for page in range(60, MAX_PAGE + 1):
    print('page =', page)
    driver.get(URL.format(page))
    videos = []
    for x in driver.find_elements_by_css_selector('h2.news-t > a'):
        videos.append(x.get_attribute('href'))
    for video in videos:
        driver.get(video)
        video_url = driver.find_element_by_css_selector('#my-video_html5_api').get_attribute('src')
        print(video_url)
        with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
            fp.write(video_url + "\n")

