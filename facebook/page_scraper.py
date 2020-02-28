import argparse
import datetime
import json
import logging as log
import os
import random
import re
import time
from builtins import set

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

try:
    from facebook.settings import *
except:
    from settings import *

FB_HOME = "https://mbasic.facebook.com/"
log.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=log.INFO)

if PROXY:
    os.environ['http_proxy'] = PROXY
    os.environ['https_proxy'] = PROXY


def get_driver(username, password):
    options = Options()
    options.headless = HEADLESS
    # options.add_argument("--start-maximized")
    profile = webdriver.FirefoxProfile()
    # We set the coordinate of where we want to be.
    if FAKE_LOCATION:
        profile.set_preference("geo.wifi.uri",
                               'data:application/json, {"location": {"lat": 21.022945, "lng": 105.779009}, "accuracy": 90.0}')
    # This line is necessary to avoid to prompt for geolocation authorization.
    profile.set_preference("geo.prompt.testing", True)
    driver = webdriver.Firefox(profile, options=options)
    # login
    driver.get('https://mbasic.facebook.com/')
    driver.find_element_by_css_selector('#m_login_email').send_keys(username)
    driver.find_element_by_css_selector('.bo').send_keys(password)
    driver.find_element_by_css_selector('.bq').click()
    try:
        driver.find_element_by_css_selector('#m_login_email')
        log.error("Login failed!")
        driver.close()
        exit(0)
    except NoSuchElementException:
        log.info("Login success!")
        # Go throung login with one tap
        if re.match(r'.+facebook\.com\/login\/save-device.+', driver.current_url):
            for ele in driver.find_elements_by_css_selector('input'):
                if 'OK' in ele.text:
                    ele.click()
                    break
    except:
        log.error("Exception occurred", exc_info=True)
        driver.quit()
        exit(0)
    return driver


class PageScraper:
    def __init__(self, username, password, page_id, output):
        if USE_VIRTUAL_DISPLAY:
            self.display = Display(visible=0, size=(1366, 768))
            self.display.start()
        self.driver = get_driver(username, password)
        self.page_id = page_id
        self.output = output
        self.post_count = 0
        self.post_id_old = set()
        self.current_year = datetime.datetime.now().year
        self.scrap_page(FB_HOME + self.page_id)

    def make_a_request(self, url):
        st = random.randint(MIN_DELAY_TIME, MAX_DELAY_TIME)
        log.info('Sleep {}s before next request!'.format(st))
        time.sleep(st)
        self.driver.get(url)

    def check_not_duplicate(self, post_id):
        if post_id not in self.post_id_old:
            self.post_id_old.add(post_id)
            return True
        return False

    def save_data(self, dict_data):
        if self.check_not_duplicate(dict_data.get('post_id')):
            self.post_count += 1
            log.info('Save post #{}, post_id = {}, post_date = {}'.format(self.post_count, dict_data.get('post_id'),
                                                                          dict_data.get('post_date')))
            with open(self.output, 'a+', encoding='utf8') as fp:
                fp.write(json.dumps(dict_data, ensure_ascii=False) + '\n')
        else:
            log.warning(
                'Duplicate post #{}, post_date = {}'.format(dict_data.get('post_id'), dict_data.get('post_date')))

    def scrap_page(self, url):
        self.make_a_request(url)
        # scroll to end of page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for post in self.driver.find_elements_by_xpath("//div[contains(@data-ft,'top_level_post_id')]"):
            post_id = json.loads(post.get_attribute('data-ft'))['top_level_post_id']
            try:
                # Some post not have date: #3
                # https://mbasic.facebook.com/MTP.Fan?sectionLoadingID=m_timeline_loading_div_1583049599_0_36_timeline_unit%3A1%3A00000000001562385759%3A04611686018427387904%3A09223372036854775718%3A04611686018427387904&unit_cursor=timeline_unit%3A1%3A00000000001562385759%3A04611686018427387904%3A09223372036854775718%3A04611686018427387904&timeend=1583049599&timestart=0&tm=AQB48eDPjDi3cnb2&refid=17
                post_date = post.find_element_by_css_selector('abbr').text
            except:
                post_date = 'Date Not Found'
            for a_tag in post.find_elements_by_tag_name('a'):
                if 'Full Story' in a_tag.text:
                    post_url = re.sub(r'(/story\.php\?story_fbid=\d+&id=\d+).+', r'\1', a_tag.get_attribute('href'))
            self.save_data({'post_id': post_id, 'post_url': post_url, 'post_date': post_date})

        # scan for next page
        next_url = None
        for item in self.driver.find_elements_by_css_selector(
                '#structured_composer_async_container > div > a'):
            # if has show more
            if 'Show more' in item.text:
                log.info('Found show more! Continue...')
                next_url = item.get_attribute('href')
                break
            elif str(self.current_year) in item.text:
                log.info('Show more not found! Click on {} link!'.format(self.current_year))
                next_url = item.get_attribute('href')
                self.current_year -= 1
                break
        # 2004 is FB birthday, some page has break year(Show more, 2017,2016,...)
        while self.current_year > 2003 and not next_url:
            self.current_year -= 1
            for item in self.driver.find_elements_by_css_selector(
                    '#structured_composer_async_container > div > a'):
                if str(self.current_year) in item.text:
                    log.info('Show more not found! Click on {} link!'.format(self.current_year))
                    next_url = item.get_attribute('href')
                    self.current_year -= 1
                    break
        if next_url:
            self.scrap_page(next_url)
        else:
            log.info('Could not find next page! Current year is {}'.format(self.current_year))
            log.info('Found {} post!'.format(self.post_count))
            log.info('Save found post at {}'.format(self.output))
            log.info('Done.')
            self.close()

    def close(self):
        self.driver.quit()
        if USE_VIRTUAL_DISPLAY:
            self.display.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Facebook Username')
    parser.add_argument('-p', '--password', required=True, help='Facebook Password')
    parser.add_argument('-i', '--input', required=True, help='Facebook page ID')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    try:
        pc = PageScraper(args.username, args.password, args.input,
                         args.output)
    except:
        log.error("Exception occurred", exc_info=True)
        pc.close()
