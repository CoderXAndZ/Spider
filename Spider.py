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
                # 写入到txt 文档
                create_txt_write_in(title, href, abstract, 'baiduSearchResult')
            # print("获取的数组：", array_result)
        elif enumValue == 'three_six_zero':  # 360
            # soup = BeautifulSoup(html_content, 'lxml')
            # # 获取内容列表
            # companies = soup.find('div', id='main').select('ul > li')
            # # print('获取内容列表：', companies)
            #
            # array_result = []
            # for com in companies:
            #     print("com：", com)
            #     res = get_one_li_value(com)
            #     array_result.append(res)

            feed_box = wd.find_element_by_xpath("//div[contains(@id, 'main')]")
            result = feed_box.find_element_by_xpath("//ul[contains(@class, 'result')]")
            print("360结果：", result)
            # res-list
            lis = result.find_elements_by_xpath("//li[contains(@class, 'res-list')]")

            print("360的搜索结果lis：", lis)

            for i in range(0, len(lis)):
                title = lis[i].find_element_by_tag_name('h3').text
                herf = lis[i].find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')

                if title.endswith('360问答'):
                    content = lis[i].find_element_by_xpath("//div[contains(@class, 'best-ans')]").text
                else:
                    content = lis[i].find_element_by_tag_name('p').text

                print("title:", title)
                print("content:", content)
                print("链接：", herf)

                # 写入到txt 文档
                create_txt_write_in(title, herf, content, '360SearchResult')

        elif enumValue == 'search_dog':  # 搜狗
            print("搜狗")
            feed_box = wd.find_element_by_xpath("//div[contains(@class, 'results')]")

            rb_results = feed_box.find_elements_by_xpath("//div[contains(@class, 'rb')]")

            vrwrap_results = feed_box.find_elements_by_xpath("//div[contains(@class, 'vrwrap')]")

            print("长度：", len(rb_results), "搜狗结果：", rb_results )
            print("长度：", len(vrwrap_results), "搜狗-----结果：", vrwrap_results)

            for i in range(0, len(rb_results)):
                pt = rb_results[i].find_element_by_xpath("//h3[contains(@class, 'pt')]")
                title_rb = pt.text   # find_element_by_class_name('pt').text
                if is_element_exist(pt, 'a', 2):
                    href_rb = pt.find_element_by_tag_name('a').get_attribute(
                        'href')  # find_element_by_class_name('pt').find_element_by_tag_name('a').get_attribute('href')
                else:
                    href_rb = "未获取到链接"
                content_rb = rb_results[i].find_element_by_xpath("//div[contains(@class, 'ft')]").text  # find_element_by_class_name('ft').text

                print("title:", title_rb)
                print("content:", content_rb)
                print("链接：", href_rb)

                # 写入到txt 文档
                create_txt_write_in(title_rb, href_rb, content_rb, 'dogSearchResult')


            for j in range(0, len(vrwrap_results)):
                vrTitle = vrwrap_results[j].find_element_by_class_name('vrTitle')
                title = vrTitle.text
                if is_element_exist(vrTitle, 'a', 2):
                    href = vrTitle.find_element_by_tag_name('a').get_attribute('href')
                else:
                    href = "未获取到链接"
                content = vrwrap_results[j].find_element_by_xpath("//p[contains(@class, 'str_info')]").text + \
                          vrwrap_results[j].find_element_by_xpath('//ul').text

                print("title:", title)
                print("content:", content)
                print("链接：", href)

                # 写入到txt 文档
                create_txt_write_in(title, href, content, 'dogSearchResult')


            # # res-list
            # lis = result.find_elements_by_xpath("//li[contains(@class, 'biz_rb ')]")
            #
            # print("搜狗的搜索结果lis：", lis)
            #
            # for i in range(0, len(lis)):
            #     title = lis[i].find_element_by_tag_name('h3').text
            #     herf = lis[i].find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
            #
            #     if title.endswith('360问答'):
            #         content = lis[i].find_element_by_xpath("//div[contains(@class, 'best-ans')]").text
            #     else:
            #         content = lis[i].find_element_by_tag_name('p').text
            #
            #     print("title:", title)
            #     print("content:", content)
            #     print("链接：", herf)
            #
            #     # 写入到txt 文档
            #     create_txt_write_in(title, herf, content, 'dogSearchResult')

        else:  # 今日头条
            print("今日头条")  # feedBox
            feedBox = wd.find_element_by_xpath("//div[contains(@class, 'feedBox ')]")
            sections = feedBox.find_element_by_xpath("//div[contains(@class, 'sections')]")
            # sections = wd.find_elements_by_class_name('articleCard')
            print('sections:', sections)
            # articles = sections.findelements
            # ".//*[@class='alert_information']/b"  "//div[contains(@class, 'articleCard')]"
            divs = wd.find_elements_by_xpath(".//*[@class='articleCard']")
            print("divs长度：", len(divs), 'divs:', divs)

            for i in range(0, 10):
                id_str = 'J_section_' + str(i)
                path_str = str.format("//div[contains(@id, {0})]", id_str)
                every_section = sections.find_element_by_xpath(path_str)

                # div_a = every_section.find_element_by_xpath("//div[contains(@class, 'title-box')]").text
                title = every_section.text

                href = every_section.find_element_by_tag_name('a').get_attribute('href')

                print("title：", title)
                # print("div_a:", div_a)
                print("href：", href)

                # 写入到txt 文档
                create_txt_write_in(title, href, '', 'todaySearchResult')

                # a = every_section.find_element_by_xpath("//div[contains(@class, 'normal  ')]")

                # print("每一个section：", every_section)



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
def is_element_exist(tag, name, by_class):
    if by_class == 1:
        try:
            tag.find_element_by_class_name(name)
            return True
        except NoSuchElementException:
            return False
    elif by_class == 2:
        try:
            tag.find_element_by_tag_name(name)
            return True
        except NoSuchElementException:
            return False
    else:
        try:
            tag.find_element_by_xpath(name)
            return True
        except NoSuchElementException:
            return False


# if __name__ == '__main__':
#     # page_begin = input("请输入开始页码，没有输入0，点击enter：")
#     open_firefox(0, '融托金融')