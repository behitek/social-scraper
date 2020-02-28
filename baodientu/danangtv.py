from time import sleep

from selenium import webdriver

url = "http://www.drt.danang.vn/chuong_trinh-185-chao_ngay_moi"
SAVE_DIR = "data/danangtv/chao-ngay-moi.txt"
driver = webdriver.Firefox()

driver.get(url)

while True:
    for video in driver.find_elements_by_css_selector('div.TinTuc_Left_Item > a'):
        with open(SAVE_DIR, 'a+', encoding='utf8') as fp:
            fp.write('http://www.drt.danang.vn/' + video.get_attribute('data-url') + "\n")
    sleep(1)
    btn_next = driver.find_element_by_css_selector('img.dxWeb_pNext_Metropolis')

    if btn_next:
        driver.execute_script("arguments[0].click();", btn_next)
driver.close()
