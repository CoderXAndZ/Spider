#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
#

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# 浏览器
wd = webdriver.Firefox()

# 当前窗口
current_window = wd.current_window_handle


# 打开浏览器
def open_firefox(page):
    # url = 'https://www.baidu.com/s?wd=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&pn=10&oq=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&tn=monline_3_dg&ie=utf-8&usm=1&rsv_pq=8ef13f780000d1b5&rsv_t=f1a8letyGDxgzrFTe%2BTXGUVodY1icqi2d3bmB8S9WJqSkjL80kJTOnwlAdr6nkpPNWPb&rsv_page=1'


    global current_page
    url = 'https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D'
    try:
        page_num = '?page=%s' % page
        current_page = int(page)
        wd.get(url+page_num)
        wait = WebDriverWait(wd, timeout=13)
        # # wait.until(expected_conditions.title_is("京东试用-专业的综合网上免费试用平台"))
        # # wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, '.link-login'))
    except NoSuchElementException as e:
        print("异常信息：", e.msg)


# 判断元素是否存在
def is_element_exist(name, by_class):
    if by_class:
        try:
            wd.find_element_by_class_name(name)
            return True
        except NoSuchElementException:
            return False
    else:
        try:
            wd.find_element_by_xpath(name)
            return True
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    page_begin = input("请输入开始页码，没有输入0，点击enter：")
    open_firefox(page_begin)