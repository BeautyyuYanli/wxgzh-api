from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import sys
import time
import json
import urllib
import os
from xvfbwrapper import Xvfb
delay = int(os.getenv('DELAY'))


def get_by_css(driver, cssstr, multi=0, button=0):
    try:
        if button == 0:
            myElem = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssstr)))
        else:
            myElem = [WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssstr)))]
        if multi == 1:
            return myElem
        else:
            return myElem[0]
    except:
        return 0


def publish(appid=0):
    # load driver and cookies
    # vdis = Xvfb()
    # vdis.start()
    try:
        os.remove('geckodriver.log')
    except:
        pass
    options = Options()
    options.log.level = "trace"
    driver = webdriver.Firefox(options=options)
    with open('cookies.json', 'r') as f:
        cookies = f.read()
    cookies = json.loads(cookies)
    driver.get('https://mp.weixin.qq.com/')
    for i in cookies:
        driver.add_cookie(i)
    time.sleep(delay / 3)
    driver.get('https://mp.weixin.qq.com/')
    real_url = driver.current_url
    token = urllib.parse.parse_qs(real_url)['token'][0]
    # check list and get appid
    driver.get('https://mp.weixin.qq.com/cgi-bin/appmsg?begin=0&count=10&type=77&action=list_card&token={}&lang=zh_CN'.format(token))
    appid = get_by_css(
        driver, 'div.publish_card_container:nth-child(2) > div:nth-child(1)').get_attribute('data-appid')
    # publish
    try:
        driver.get('https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&appmsgid={}&isMul=1&replaceScene=0&isSend=1&isFreePublish=0&token={}&lang=zh_CN'.format(appid, token))
        get_by_css(
            driver, '.mass-send__footer .weui-desktop-btn_primary', button=1).click()
        al = get_by_css(
            driver, '#vue_app > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > button', button=1)
        print(al)
        al.click()
        time.sleep(delay * 3)
    except:
        print('error when publishing')
        return -1

    driver.close()
    # vdis.stop()
    return 0


if __name__ == "__main__":
    publish()
