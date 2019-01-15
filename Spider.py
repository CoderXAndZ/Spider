#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
#

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# 浏览器
wd = webdriver.Firefox()

# 当前窗口
current_window = wd.current_window_handle


# 打开浏览器, 搜索关键字
def open_firefox(page, keywords):
    # url = 'https://www.baidu.com/s?wd=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&pn=10&oq=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&tn=monline_3_dg&ie=utf-8&usm=1&rsv_pq=8ef13f780000d1b5&rsv_t=f1a8letyGDxgzrFTe%2BTXGUVodY1icqi2d3bmB8S9WJqSkjL80kJTOnwlAdr6nkpPNWPb&rsv_page=1'

    global current_page
    url = 'https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D'
    try:
        # page_num = '?page=%s' % page
        current_page = int(page)
        # wd.get(url+page_num)
        wd.get(url)
        wait = WebDriverWait(wd, timeout=13)
        # # wait.until(expected_conditions.title_is("平台"))
        # # wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, '.link-login'))

        # print("页面内容：", wd.page_source)
        # 获取页面内容
        html_content = wd.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        # 获取内容列表
        companies = soup.find('div', id='content_left')
        print('获取内容列表：', companies)
        array_result = []
        for i in range(1, 10):
            div_one = companies.find('div', id=str(i))
            array_result.append(div_one)
            # h3标签中的a链接的内容
            title = div_one.find('h3', class_='t').a.contents  # 题目  a.contents 获取链接的内容
            title = str(title).replace('<em>', '').replace('</em>', '')  # 删除<em> 和 </em>
            href = div_one.find('h3', class_='t').a['href']  # 链接
            abstract = div_one.find('div', class_='c-abstract')  # 内容 .contents
            if abstract is not None:
                # 去除其他字符，只剩文字
                abstract = str(abstract.contents).replace('<div class="c-abstract">', '').\
                    replace('</div>', '').replace('<em>', '').replace('</em>', '').\
                    replace('<span class="newTimeFactor_before_abs m">', '').replace('</span>', '').replace('\'', '')
            else:
                abstract = "无"
            print("title是：", title)
            print("href链接是：", href)
            print("abstract简介是：", abstract)
            create_txt_write_in(title, href, abstract)
        # print("获取的数组：", array_result)

    except NoSuchElementException as e:
        print("异常信息：", e.msg)


# 创建txt文件，逐行写入
def create_txt_write_in(title, href, abstract):
    txt_name = "searchResult.txt"
    f = open(txt_name, "a+")
    f.write('标题：' + title + '\n')
    f.write('链接：' + href + '\n')
    f.write('简介：' + abstract + '\n\n')
    f.close()


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
    # page_begin = input("请输入开始页码，没有输入0，点击enter：")
    open_firefox(0, '融托金融')