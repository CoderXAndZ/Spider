#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
#

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# 打开浏览器, 搜索关键字
def open_firefox(page, keywords, browser_type, enumValue):
    # 浏览器
    global wd
    wd = webdriver.Firefox()

    # 当前窗口
    current_window = wd.current_window_handle

    # url = 'https://www.baidu.com/s?wd=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&pn=10&
    # oq=%E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D&tn=monline_3_dg&ie=utf-8&usm=1&rsv_pq=8ef13f780000d1b5&rsv_t=f1a8letyGDxgzrFTe%2BTXGUVodY1icqi2d3bmB8S9WJqSkjL80kJTOnwlAdr6nkpPNWPb&rsv_page=1'
    global current_page

    # %E8%9E%8D%E6%89%98%E9%87%91%E8%9E%8D
    url = browser_type + keywords
    print("搜索url:", url)
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

        if enumValue == 'bai_du':  # 百度搜索
            soup = BeautifulSoup(html_content, 'html.parser')
            # 获取内容列表
            companies = soup.find('div', id='content_left')
            # print('获取内容列表：', companies)
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
                create_txt_write_in(title, href, abstract, 'baiduSearchResult')
            # print("获取的数组：", array_result)
        elif enumValue == 'three_six_zero':  # 360
            soup = BeautifulSoup(html_content, 'lxml')
            # 获取内容列表
            companies = soup.find('div', id='main').select('ul > li')
            # print('获取内容列表：', companies)

            array_result = []
            for com in companies:
                print("com：", com)
                res = get_one_li_value(com)
                array_result.append(res)

            # title = companies[0].h3.a.contents
            #     # find('h3', class_='res-title ')  # 题目  a.contents 获取链接的内容
            # href = companies[0].h3.a['href']  # 链接
            # abstract = companies[0].p.contents  # 内容
            # print('title：', title)
            # print('href：', href)
            # print('abstract：', abstract)
            # print('href:', href)
            # print('abstract:', abstract)


            # ul = wd.find_element_by_xpath('//*[@id="main"]/ul')
            # li_lists = ul.find_elements_by_xpath('li')
            # print("li_lists", li_lists)
            #
            # for li in li_lists:
            #     link_a = li.find_elements_by_xpath("//h3[contains(@class, 'res-title ')]/a")
            #     title = link_a[0].text
            #     href = link_a
            #
            #     print("title:", title)
            #     # for value in title:
            #     #     print("title:", value.text)
            #     # print("com:", com)
            #     # res = get_one_li_value(com)
            #     # array_result.append(res)

        elif enumValue == 'search_dog':  # 搜狗
            soup = BeautifulSoup(html_content, 'lxml')
            print('搜狗')
        else:  # 今日头条
            print("今日头条")
            sections = wd.find_elements_by_xpath("//div[contains(@class, 'articleCard')]")
            # sections = wd.find_elements_by_class_name('articleCard')
            print('sections:', sections)


            # soup = BeautifulSoup(html_content, 'html.parser')
            # # 获取内容列表
            # companies = soup.find('div', class_='sections')
            # print('获取内容列表：', companies)

            array_result = []
            # for i in range(0, 20):
            #     com = companies[i]
            #     id_text = "J_section_" + str(i)
            #     title = com.find('div', classs_='title-box').a.get_text()
            #     print("com：", com)
            #     print("title:", title)
            #     # array_result.append(res)

    except NoSuchElementException as e:
        print("异常信息：", e.msg)


# 获取一条信息
def get_one_li_value(soup):
    # mainx = soup.find_element_by_xpath(soup, "//div[contains(@id, 'main')]")
    #
    # print("maindx:", mainx)

    abstract = ''
    # h3标签中的a链接的内容
    title = soup.select('li > h3')
    if is_exist_a(title):
        title = soup.h3.a.get_text()   # 题目  a.contents 获取链接的内容
        href = soup.h3.a['href']  # 链接
    else:
        href = soup.h3  # 链接
    title = str(title)

    if is_exist_p(soup):
        abstract = str(soup.p.get_text())
    elif is_exist_div(soup):
        abstract = str(soup.div.contents).replace('<em>', '').replace('</em>', '')  # 内容

    print("title是：", title)
    print("href链接是：", href)
    print("abstract简介是：", abstract)
    create_txt_write_in(title, str(href), str(abstract), '360SearchResult')
    return [title, href, abstract]


# 查看是否包含 a 标签
def is_exist_a(label):
    try:
        label.a.attrs
        print("查看是否包含 a 标签")
        return True
    except AttributeError:
        return False


# 查看是否包含 p 标签
def is_exist_p(label):
    try:
        label.p.attrs
        print("查看是否包含 p 标签")
        return True
    except AttributeError:
        return False


# 查看是否包含 p 标签
def is_exist_div(label):
    try:
        label.div.attrs
        print("查看是否包含 div 标签")
        return True
    except AttributeError:
        return False


# 创建txt文件，逐行写入
def create_txt_write_in(title, href, abstract, txt_name):
    txt_name = txt_name + ".txt"
    f = open(txt_name, "a+")  # r+ 覆盖  a+ 追加  .truncate()
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


# if __name__ == '__main__':
#     # page_begin = input("请输入开始页码，没有输入0，点击enter：")
#     open_firefox(0, '融托金融')