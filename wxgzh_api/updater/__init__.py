from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
import time
import json
import urllib
from dateutil.parser import isoparse
from .exceptions import CookieException


class Updater:
    def __init__(self, cookiefile: str | None = None, cookies: dict | None = None, loglevel: str = "warn", headless: bool = True) -> None:
        # Load driver and cookies
        options = Options()
        options.log.level = loglevel
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)
        if cookies == None:
            with open(cookiefile if cookiefile else "cookies.json", 'r') as f:
                cookies = f.read()
            cookies = json.loads(cookies)
        self.driver.get('https://mp.weixin.qq.com/')
        for i in cookies:
            self.driver.add_cookie(i)
        # Magic delay
        time.sleep(1)
        # Refresh the page
        self.driver.get('https://mp.weixin.qq.com/')
        self.get_by_css('#footer.mp-foot')
        real_url = self.driver.current_url
        if real_url.split('qq.com')[1] == '/':
            raise CookieException(
                "Not logged in. Maybe the cookie is expired?")
        token = urllib.parse.parse_qs(real_url)['token'][0]
        editor_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token=' + token + '&lang=zh_CN'
        self.driver.get(editor_url)
        self.get_by_css('#js_text_editor_tool_link').click()

    def __del__(self) -> None:
        self.driver.quit()
        pass

    def get_by_css(self, css: str, multi: bool = False, base_elem: WebElement | None = None) -> List[WebElement] | WebElement | None:
        try:
            myElem = WebDriverWait(base_elem if base_elem else self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css)))
            if multi == True:
                return myElem
            else:
                return myElem[0]
        except:
            None

    def update(self, subscribe_list: List[str]):
        update_pool = {}

        # search for articles
        for entry in subscribe_list:
            update_pool[entry] = []
            othergzh_button = self.get_by_css(
                '.weui-desktop-btn.weui-desktop-btn_default')
            othergzh_button.click()

            input_box = self.get_by_css(
                '.weui-desktop-form__input_append-in > input')
            input_box.send_keys(entry)
            input_box.send_keys(Keys.ENTER)

            flag = 0
            for i in range(5):
                gzh_entry = self.get_by_css(
                    'ul.inner_link_account_list > li:nth-child({})'.format(i+1))
                if gzh_entry == 0:
                    break
                if self.get_by_css(
                    'ul.inner_link_account_list > li:nth-child({}) strong'.format(
                        i+1)
                ).text == entry:
                    flag = 1
                    break
            if flag == 0:
                gzh_entry = self.get_by_css(
                    'ul.inner_link_account_list > li:nth-child(1)')
                print('no match for {}, got:'.format(entry))
                print(self.get_by_css(
                    'ul.inner_link_account_list > li:nth-child(1) strong').text)
            gzh_entry.click()
            article_entries: List[WebElement] = self.get_by_css(
                '.inner_link_article_item', True)
            for article_entry in article_entries:
                link_element = self.get_by_css(
                    'label.inner_link_article_item > span:nth-child(3) > a', base_elem=article_entry)
                title_element = self.get_by_css(
                    'div.inner_link_article_title > span:nth-child(2)', base_elem=article_entry)
                date_element = self.get_by_css(
                    'div.inner_link_article_date', base_elem=article_entry)
                link = link_element.get_attribute('href')
                title = title_element.get_attribute('innerHTML')
                date = date_element.get_attribute('innerHTML')
                # it is compatible with JSON feeds 1.1 item
                update_pool[entry].append(
                    {
                        "url": link,
                        "title": title,
                        "authors": [{"name": entry}],
                        "date_published": isoparse("2023-03-05 +08").isoformat()
                    })

        return (update_pool)


if __name__ == "__main__":
    subscribe_list = [
        '大连理工大学',
    ]
    updater = Updater(cookiefile='cookies.json',
                      loglevel="trace", headless=True)
    msg = updater.update(subscribe_list)
    print(msg)
