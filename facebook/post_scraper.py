import argparse
import json
import logging as log
import os
import random
import re
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

try:
    from facebook.settings import *
except:
    from settings import *

FB_HOME = "https://mbasic.facebook.com/"
log.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=log.WARNING)

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
    # time.sleep(100)
    try:
        driver.find_element_by_css_selector('#m_login_email')
        log.error("Login failed!")
        driver.close()
        exit(0)
    except NoSuchElementException:
        log.warning("Login success!")
        # Go throung login with one tap
        if re.match(r'.+facebook\.com\/login\/save-device.+', driver.current_url):
            for ele in driver.find_elements_by_css_selector('input'):
                if 'OK' in ele.text:
                    ele.click()
                    break
    except:
        log.error("Exception occurred", exc_info=True)
        driver.close()
        exit(0)
    return driver


class PostScraper:
    def __init__(self):
        if USE_VIRTUAL_DISPLAY:
            self.display = Display(visible=0, size=(1366, 768))
            self.display.start()
        self.driver = None

    def set_driver(self, driver):
        self.driver = driver

    def make_a_request(self, url):
        st = random.randint(MIN_DELAY_TIME, MAX_DELAY_TIME)
        # log.info('Sleep {}s before next request!'.format(st))
        time.sleep(st)
        self.driver.get(url)

    @staticmethod
    def save_data(dict_data, file_path):
        with open(file_path, 'a+', encoding='utf8') as fp:
            fp.write(json.dumps(dict_data, ensure_ascii=False) + '\n')

    def scrap_post(self, url, output_file):
        self.make_a_request(url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        more_comment_url = None
        reply_comment_urls = []
        for comment_obj in self.driver.find_elements_by_css_selector(
                '#m_story_permalink_view > div:nth-child(2) > div > div:nth-child(5) > div'):
            if len(comment_obj.get_attribute('class')) == 2 and re.match("\\d+", comment_obj.get_attribute('id')):
                author = comment_obj.find_element_by_css_selector('h3 > a').text
                author_url = comment_obj.find_element_by_css_selector('h3 > a').get_attribute('href')
                text = comment_obj.find_element_by_css_selector(
                    'div[id="{}"] > div > div'.format(comment_obj.get_attribute('id'))).text
                self.save_data({'author': author, 'author_url': author_url, 'text': text, 'reply_to': 'ROOT'},
                               output_file)

                # Check if has nested comment (reply)
                for ele in comment_obj.find_elements_by_css_selector('a'):
                    if ele.get_attribute('href') is not None and '/comment/replies' in ele.get_attribute(
                            'href') and '&count=' in ele.get_attribute('href'):
                        reply_comment_urls.append((ele.get_attribute('href'), author))
                        break
            # Get view more comment url
            if 'see_next' in comment_obj.get_attribute('id') and 'View more' in comment_obj.text:
                more_comment_url = comment_obj.find_element_by_css_selector('a').get_attribute('href')
        if len(reply_comment_urls):
            log.info('Start crawl {} reply url!'.format(len(reply_comment_urls)))
        for reply_comment_url, root in reply_comment_urls:
            self.__scrap_reply__(reply_comment_url, root, output_file)
        if more_comment_url:
            log.info('Found view mores comments! Continue...')
            self.scrap_post(more_comment_url, output_file)
        else:
            log.info('View more comments not found!')
            log.info('Done.')

    def __scrap_reply__(self, reply_url, root, output_file):
        log.info('\tCrawl comment in reply page...')
        self.make_a_request(reply_url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        more_reply_url = None
        for reply_obj in self.driver.find_elements_by_css_selector('div#root > div > div:nth-child(3) > div'):
            if len(reply_obj.get_attribute('class')) == 2 and re.match("\\d+", reply_obj.get_attribute('id')):
                author = reply_obj.find_element_by_css_selector('h3 > a').text
                author_url = reply_obj.find_element_by_css_selector('h3 > a').get_attribute('href')
                text = reply_obj.find_element_by_css_selector(
                    'div[id="{}"] > div > div'.format(reply_obj.get_attribute('id'))).text
                self.save_data({'author': author, 'author_url': author_url, 'text': text, 'reply_to': root},
                               output_file)
            if 'comment_replies' in reply_obj.get_attribute('id') and 'View next' in reply_obj.text:
                more_reply_url = reply_obj.find_element_by_css_selector('a').get_attribute('href')
        if more_reply_url:
            log.info('\t\tFound view mores replies! Continue...')
            self.__scrap_reply__(more_reply_url, root, output_file)
        else:
            log.info('\tView mores replies not found! Done. Go back...')

    def destroy_driver(self):
        self.driver.quit()

    def close(self):
        if USE_VIRTUAL_DISPLAY:
            self.display.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Facebook Username')
    parser.add_argument('-p', '--password', required=True, help='Facebook Password')
    parser.add_argument('-i', '--input', required=True, help='Input file path (Output of me_page_scraper.py)')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-n', '--nline', type=int, default=0, help='Checkpoint (For re-run)')
    check_point = ''
    args = parser.parse_args()
    pc = PostScraper()
    try:
        lines = open(args.input).read().splitlines()
        for idx, line in enumerate(lines):
            if idx + 1 < args.nline:
                continue
            post_url = json.loads(line).get('post_url')
            pc.set_driver(get_driver(args.username, args.password))
            check_point = 'Crawl post n = {} / {}, url = {}'.format(idx + 1, len(lines), post_url)
            log.warning(check_point)
            try:
                pc.scrap_post(post_url, args.output)
            except:
                log.error("Exception occurred", exc_info=True)
            pc.destroy_driver()
    except:
        log.error("Exception occurred", exc_info=True)
        pc.close()
    finally:
        with open(args.input + '.ckp', 'w', encoding='utf8') as fp:
            fp.write(check_point)
