#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 页面画

import tkinter as tk
from tkinter import *
import Spider
from tkinter import messagebox
from enum import Enum, unique  # 枚举


@unique
class Browser(Enum):  # Browser.bai_du.value 获取值;  Browser.bai_du.name  获取key;
    bai_du = 'https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd='   # 百度
    three_six_zero = 'https://www.so.com/s?ie=utf-8&src=hao_360so_b&shb=1&q='  # 360  &hsid=a6aaaf3a569fd3e6
    search_dog = 'https://www.sogou.com/web?_asf=www.sogou.com&_ast=&w=01019900&p=40040100' \
                 '&ie=utf8&from=index-nologin&s_from=index&sut=5541' \
                 '&sst0=1547608386476&lkt=0%2C0%2C0&sugsuv=1547608378959037&sugtime=1547608386476&query='   # 搜狗
    today_headline = 'https://www.toutiao.com/search/?keyword='  # 今日头条
    # net_ease = ''  # 网易


# 初始化页面
def setup_view():
    root = tk.Tk()  # 创建父容器GUI
    root.title("搜索结果")  # 父容器标题
    root.geometry("460x380")  # 设置父容器窗口初始大小，如果没有这个设置，窗口会随着组件大小的变化而变化

    # 输入关键字
    tk.Label(root, text="请输入关键字：").grid(row=1, column=0)
    keyword = StringVar()
    tk.Entry(root, textvariable=keyword).grid(row=1, column=1)
    # 百度
    tk.Button(root, text="百度", command=lambda: judge_keyword(keyword.get(), Browser.bai_du.value,
                                                             Browser.bai_du.name)).grid(row=2, column=0, pady=2)
    # 360
    tk.Button(root, text="360", command=lambda: judge_keyword(keyword.get(), Browser.three_six_zero.value,
                                                              Browser.three_six_zero.name)).grid(row=2, column=1, pady=2)
    # 搜狗
    tk.Button(root, text="搜狗", command=lambda: judge_keyword(keyword.get(), Browser.search_dog.value,
                                                             Browser.search_dog.name)).grid(row=2, column=2, pady=2)
    # 今日头条
    tk.Button(root, text="今日头条", command=lambda: judge_keyword(keyword.get(), Browser.today_headline.value,
                                                               Browser.today_headline.name)).grid(row=2, column=3, pady=2)
    # # 网易
    # tk.Button(root, text="网易", command=lambda: judge_keyword(keyword.get())).grid(row=2, column=3, pady=2)

    root.mainloop()


# 判断输入框是否有值
def judge_keyword(user_input, browser_type, enumValue):
    if user_input == '':
        Spider.open_firefox(0, '融托金融', browser_type, enumValue)
    else:
        Spider.open_firefox(0, user_input, browser_type, enumValue)


if __name__ == '__main__':
    setup_view()
