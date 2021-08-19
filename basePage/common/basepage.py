import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os.path
from basePage.common.WtLog import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from random import choice
import configparser
from selenium import webdriver



class BasePage(object):
    "定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类"

    def __init__(self,url):
        config = configparser.ConfigParser()
        dir = os.path.abspath('.').split('basePage')[0]
        config.read(dir + "/basePage/config/config.ini")
        browser = config.get("browserType", "browserName")
        log_public("You had select %s browser." % browser)
        if browser == "Firefox":
            self.driver = webdriver.Firefox()
        elif browser == "Chrome":
            self.driver = webdriver.Chrome()
        elif browser == "IE":
            self.driver = webdriver.Ie()
        self.driver.set_window_size(1920, 1080)  # 分辨率
        # self.driver.maximize_window()#最大化
        self.driver.get(url)

    def open_url(self,url):
        self.driver.get(url)


    #获取当前浏览器的url
    def get_current_url(self):
        return self.driver.current_url


    # 关闭浏览器
    def quit_browser(self):
        self.driver.quit()

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()

    # 浏览器后退操作
    def back(self):
        self.driver.back()

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)


    # 查找元素
    def find_element(self, selector):
        element = ''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]
        if selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                log_public("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                log_public("NoSuchElementException: %s" % e)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == 'css_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        elif selector_by == 'classname':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                log_public("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                log_public("NoSuchElementException: %s" % e)
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")
        return element

    # 输入
    def input(self, selector, text):
        el = self.find_element(selector)
        try:
            el.clear()
            el.send_keys(text)
            log_public("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            log_public("Failed to type in input box with %s" % e)

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        log_public("Sleep for %d seconds" % seconds)

    # 点击
    def click(self, selector):
        el = self.find_element(selector)
        try:
            el.click()
            # log_public("The element \' %s \' was clicked." % el.text)
        except NameError as e:
            log_public("Failed to click the element with %s" % e)

            # 切到iframe

    def switch_frame(self):
        iframe = self.find_element('classname=>embed-responsive-item')
        try:
            self.driver.switch_to_frame(iframe)
            # log_public("The element \' %s \' was clicked." % iframe.text)
        except NameError as e:
            log_public("Failed to click the element with %s" % e)

            # 处理标准下拉选择框,随机选择

    def select(self, id):
        select1 = self.find_element(id)
        try:
            options_list = select1.find_elements_by_tag_name('option')
            del options_list[0]
            s1 = choice(options_list)
            Select(select1).select_by_visible_text(s1.text)
            log_public("随机选的是：%s" % s1.text)
        except NameError as e:
            log_public("Failed to click the element with %s" % e)

    # 执行js
    def execute_js(self, js):
        self.driver.execute_script(js)

    # 模拟回车键
    def enter(self, selector):
        e1 = self.find_element(selector)
        e1.send_keys(Keys.ENTER)
        # 模拟鼠标左击

    def leftclick(self, element):
        # e1 = self.find_element(selector)
        ActionChains(self.driver).click(element).perform()

    # 截图，保存在根目录下的screenshots
    def take_screenshot(self):
        screen_dir = os.path.dirname(os.path.abspath('../..')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screen_name = screen_dir + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            log_public("Had take screenshot and saved!")
        except Exception as e:
            log_public("Failed to take screenshot!", format(e))

    def isElementExist(self, xpath):
        flag = True
        driver = self.driver
        try:
            driver.find_element_by_xpath(xpath)
            return flag
        except:
            flag = False
            return flag


if __name__=="__main__":
    my_base_page = BasePage('https://www.baidu.com')
    #my_base_page.open_url('www.baidu.com')
    print(my_base_page.get_current_url())
    my_base_page.quit_browser()
