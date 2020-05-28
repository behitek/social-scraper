import json
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

artists = []


def to_end_of_page(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Lấy danh sách nghệ sỹ
# driver.get('https://zingmp3.vn/the-loai-nghe-si/Kpop/IWZ9Z08W.html')
# to_end_of_page(driver)
#
# for artist in driver.find_elements_by_css_selector('#main-body > section > div > div > div > div'):
#     try:
#         url = artist.find_element_by_css_selector('div.card-info > div.artist > a').get_attribute('href')
#         name = artist.find_element_by_css_selector('div.card-info > div.artist > a').text
#         follow = artist.find_element_by_css_selector('div.follow').text
#
#         artists.append({'name': name, 'url': url, 'follow': follow, 'song': []})
#     except:
#         traceback.print_exc()

# Lấy danh sách bài hát theo từng ca sỹ

vi_articles = json.load(open('vi_artists_full.json', encoding='utf8'))

for idx, artist in enumerate(vi_articles):
    if artist.get('song'):
        continue
    url = artist.get('url')
    time.sleep(0.5)
    driver.get(url)
    time.sleep(2)
    song_url = None
    while True:
        for li in driver.find_elements_by_css_selector(
                'ul.s-sec > li'):
            if 'Bài Hát' in li.text:
                song_url = li.find_element_by_css_selector('a').get_attribute('href')
                break
        if song_url:
            break
        else:
            time.sleep(0.1)
    driver.get(song_url)
    to_end_of_page(driver)
    songs = []
    for song in driver.find_elements_by_css_selector(
            'div.card-info > div.title > a.--z--multiple-line'):
        name = song.text
        vi_articles[idx].get('song').append(name)
    print(artist.get('name'), len(vi_articles[idx].get('song')))
with open('vi_artists_full1.json', 'w', encoding='utf8') as fp:
    json.dump(vi_articles, fp, ensure_ascii=False)

driver.quit()
