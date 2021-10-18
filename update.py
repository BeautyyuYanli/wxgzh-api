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
    try:
        myElem = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssstr)))
        if multi == 1:
            return myElem
        else:
            return myElem[0]
    except:
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
    options.log.level = "trace"
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
        get_by_css(driver, '#footer.mp-foot')
        real_url = driver.current_url
        if real_url.split('qq.com')[1] == '/':
            raise ValueError('cookies error!')
        token = urllib.parse.parse_qs(real_url)['token'][0]
        editor_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token=' + token + '&lang=zh_CN'
        driver.get(editor_url)
        get_by_css(driver, '#js_text_editor_tool_link').click()

        # search for articles
        for entry in subscribe_list:
            update_pool[entry] = []
            othergzh_button = get_by_css(driver, '.weui-desktop-btn.weui-desktop-btn_default')
            if othergzh_button != 0:
                othergzh_button.click()
            input_box = get_by_css(driver, '.weui-desktop-form__input_append-in > input')
            input_box.send_keys(entry)
            input_box.send_keys(Keys.ENTER)
            flag = 0
            for i in range(5):
                gzh_entry = get_by_css(driver, 'ul.inner_link_account_list > li:nth-child({})'.format(i+1))
                if gzh_entry == 0:
                    break
                if get_by_css(
                    driver, 
                    'ul.inner_link_account_list > li:nth-child({}) strong'.format(i+1)
                    ).text == entry:
                    flag = 1
                    break
            if flag == 0:
                update_pool[entry].append({"title": "no gzh found", "link": "http://example.com", "author": entry, "date": "1970-01-01"})
                continue
            gzh_entry.click()
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
    return(update_pool)

if __name__ == "__main__":
    subscribe_list = [
        '大连理工大学',
    ]
    update(subscribe_list)
