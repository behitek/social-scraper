import os
import random
import traceback
import uuid
from datetime import datetime
from time import sleep

import wget
from selenium import webdriver

URL = "https://subscene.com/browse"
SAVE_DIR = "/home/lap60313/data/vpbank/subtitle/film/"

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", SAVE_DIR)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/pdf, application/octet-stream, application/x-winzip, application/x-pdf, application/x-gzip")
driver = webdriver.Firefox(firefox_profile=profile)

driver.get(URL)

# changle languge
edit_button = driver.find_element_by_css_selector('#content > div.box.byFilm > div > div.language-filter > small > a')
edit_button.click()

select_ckb = driver.find_element_by_css_selector(
    '#content > div > div > form > div:nth-child(2) > div:nth-child(22) > label > input[type=checkbox]')
select_ckb.click()

driver.find_element_by_css_selector('#content > div > div > form > div:nth-child(3) > button').click()

CRAWLED_DATE_LOG = "do_not_remove.date.film"
# get latest crawl date
crawled_date = '12/4/2019 10:37:00 AM'
try:
    crawled_date = open(CRAWLED_DATE_LOG).read()
except:
    pass
crawled_date = datetime.strptime(crawled_date, '%m/%d/%Y %I:%M:%S %p')
latest_crawl_date = crawled_date

print('Crawled_date is {}'.format(crawled_date))
print('Start crawling new data...')
for i in range(1, 101):
    print('Download FILM PAGE = {}'.format(i))
    try:
        url = "https://subscene.com/browse/latest/film/{}".format(i)
        driver.get(url)
        items = driver.find_elements_by_css_selector('#content > div.box.byFilm > div > table > tbody > tr')
        download_list = []
        for item in items:
            url = item.find_element_by_css_selector('td.a1 > a').get_attribute('href')
            title = item.find_element_by_css_selector('span.new').text.strip()
            time_log = item.find_element_by_css_selector('td.a6 > div').get_attribute('title').strip()
            if latest_crawl_date == crawled_date:
                latest_crawl_date = datetime.strptime(time_log, '%m/%d/%Y %I:%M:%S %p')
            download_list.append(
                (url, SAVE_DIR + uuid.uuid4().hex + '.zip', datetime.strptime(time_log, '%m/%d/%Y %I:%M:%S %p')))
        for url, save_path, log_time in download_list:
            if log_time <= crawled_date:
                print('Got crawled date! Exit now...')
                driver.close()
                with open(CRAWLED_DATE_LOG, 'w') as fp:
                    print('Save latest crawl date!')
                    fp.write(latest_crawl_date.strftime('%m/%d/%Y %I:%M:%S %p'))
                    print('Done!')
                exit(0)
            try:
                driver.get(url)
                url = driver.find_element_by_css_selector('#downloadButton').get_attribute('href')
                os.system("wget -O {0} {1}".format(save_path, url))
                # exit(0)
                sleep(random.randint(1, 2))
            except:
                traceback.print_exc()
        sleep(random.randint(1, 3))
    except SystemExit:
        exit(0)
    except:
        traceback.print_exc()

driver.close()

with open(CRAWLED_DATE_LOG, 'w') as fp:
    print('Save latest crawl date!')
    fp.write(latest_crawl_date.strftime('%m/%d/%Y %I:%M:%S %p'))
    print('Done!')
