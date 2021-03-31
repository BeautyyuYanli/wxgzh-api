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
def get_by_css(driver, cssstr, multi=0):
    for i in range(120):
        try:
            if multi:
                element = driver.find_elements_by_css_selector(cssstr)
            else:
                element = driver.find_element_by_css_selector(cssstr)
        except:
            time.sleep(0.5)
            continue
        else:
            return element
    return 0

def update(subscribe_list):
    # load driver and cookies
    vdis = Xvfb()
    vdis.start()
    try:
        os.remove('geckodriver.log')
    except:
        pass
    options = Options()
#    options.log.level = "trace"
    driver = webdriver.Firefox(options=options)
    with open('cookies.json', 'r') as f:
        cookies = f.read()
    cookies = json.loads(cookies)
    driver.get('https://mp.weixin.qq.com/')
    for i in cookies:
        driver.add_cookie(i)
    time.sleep(delay / 3)
    update_pool = {}
    try:
        # open editor page
        driver.get('https://mp.weixin.qq.com/')
        time.sleep(delay / 3)
        real_url = driver.current_url
        if real_url.split('qq.com')[1] == '/':
            raise ValueError('coockies error!')
        token = urllib.parse.parse_qs(real_url)['token'][0]
        editor_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token=' + token + '&lang=zh_CN'
        driver.get(editor_url)
        time.sleep(delay / 3)
        driver.find_element_by_css_selector('#js_text_editor_tool_link').click()
        time.sleep(delay / 2)

        # search for articles
        for entry in subscribe_list:
            update_pool[entry] = []
            othergzh_button = get_by_css(driver, '.weui-desktop-btn.weui-desktop-btn_default')
            othergzh_button.click()
            time.sleep(delay / 2)
            input_box = get_by_css(driver, '.link_dialog_panel .weui-desktop-form__input:nth-child(2)')
            input_box.send_keys(entry)
            time.sleep(delay / 3)
            input_box.send_keys(Keys.ENTER)
            time.sleep(delay)
            gzh_entry = get_by_css(driver, '.link_dialog_panel li:nth-child(1)')
            gzh_entry.click()
            time.sleep(delay * 1.5)
            article_entries = get_by_css(driver, '.inner_link_article_item', 1)
            for article_entry in article_entries:
                link_element = get_by_css(article_entry, 'span:nth-child(3) > a')
                title_element = get_by_css(article_entry, 'div.inner_link_article_title > span:nth-child(2)')
                date_element = get_by_css(article_entry, 'div.inner_link_article_date')
                link = link_element.get_attribute('href')
                title = title_element.get_attribute('innerHTML')
                date = date_element.get_attribute('innerHTML')
                update_pool[entry].append({"title": title, "link": link, "author": entry, "date": date})
    except ValueError as msg:
        update_pool = str(msg)
    finally:
        pass

    driver.close()
    vdis.stop()
    # print(update_pool)
    return(update_pool)

if __name__ == "__main__":
    subscribe_list = [
        'dut_su',
        'iduter',
    ]
    update(subscribe_list)
