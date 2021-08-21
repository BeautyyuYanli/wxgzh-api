from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import sys, time, json, urllib, os
from xvfbwrapper import Xvfb
delay = int(os.getenv('DELAY'))
def get_by_css(driver, cssstr, multi=0, button=0):
    try:
        if button == 0:
            myElem = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssstr)))
        else:
            myElem = [WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssstr)))]
        if multi == 1:
            return myElem
        else:
            return myElem[0]
    except:
        return 0

def publish(appid=0):
    # load driver and cookies
    vdis = Xvfb()
    vdis.start()
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
    # get_by_css(driver, 'li.weui-desktop-menu__item:nth-child(2) > ul:nth-child(2) > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1)').click()
    real_url = driver.current_url
    token = urllib.parse.parse_qs(real_url)['token'][0]
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?begin=0&count=10&type=10&action=list_card&token={}&lang=zh_CN'.format(token)
    driver.get(url)
    cards = get_by_css(driver, 'tbody > tr > td > div:nth-child(1) > div:nth-child(4) > a:nth-child(1)', 1)
    # cards = get_by_css(driver, '.weui-desktop-card.weui-desktop-appmsg', 1)
    LatestAppid = cards[0].get_attribute('href')
    LatestAppid = urllib.parse.parse_qs(LatestAppid)['appmsgid'][0]
    # LatestAppid = cards[0].get_attribute('data-appid')
    if appid == 0:
        appid = LatestAppid
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid={}&token={}&lang=zh_CN&fromview=list'.format(appid, token)
    driver.get(url)
    get_by_css(driver, '#js_send', button=1).click()
    get_by_css(driver, '.mass-send__footer .weui-desktop-btn_primary').click()
    al = get_by_css(driver, '#vue_app > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > button', button=1)

    if al == 0:
        # print('error when publishing')
        return -1
    else:
        al.click()
        time.sleep(delay * 3)
        # print('done')
    driver.close()
    vdis.stop()
    return 0

if __name__ == "__main__":
    publish()
