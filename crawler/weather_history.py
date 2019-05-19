#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-30 11:50:10
# @Author  : Kian (kiangao@163.com)
# @Link    : https://www.jianshu.com/u/11e1049a308f
# @Version : 1.0

import requests
import re
import time
from bs4 import BeautifulSoup
import random
import csv
import argparse
from collections import ChainMap
from jieba import analyse
import os
import sys
from collections import namedtuple

'''
从tianqi.com中抓取历史天气，然后保存于csv文件中
'''


class TianqiHistoryCrawler(object):

    def __init__(self, city, start, end):
        self._city = city
        self._start = start
        self._end = end
        self._tianqi = []
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
        self._cookies = {'cookie': 'UM_distinctid=16aca44a6b56e-0e98a232d14ca2-6353160-144000-16aca44a6b65c2; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1558180950; cityPy=chengdu; cityPy_expire=1558785414; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1558180960; Hm_lpvt_bfc6c23974fbad0bbfed25f88a973fb0=1558186373; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1558189346; CNZZDATA1275796416=285342940-1558176756-%7C1558187565'}

    def crawlOnePage(self, html):
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        comment = {}
        tqxiangqing = soup.select('.tqxiangqing')[0]
        # print(tqxiangqing)
        for a in tqxiangqing.find_all('a'):
            if a.string == '下一天':
                # comment['next'] = a['href']
                comment['next'] = re.findall(r'http.+/(\d+)\.+', a['href'])[0]
        tqshow = soup.select('.tqshow')[0]
        lis = tqshow.find_all('li')
        comment['wind'] = lis[len(lis)-1].string

        t_temp = tqshow.select('#t_temp')[0]
        temp = []
        for a in t_temp.find_all('font'):
            temp.append(a.string)
        comment['temp'] = temp
        cDRed = soup.select('.cDRed')[0].string
        comment['tianqi'] = cDRed

        history_data_r01 = soup.select('.history_data_r01')[0]
        lis = history_data_r01.find_all('li')
        for li in lis:
            s = re.findall(r'<li>(\w+)：.+', str(li))[0]
            comment[s] = li.find_all('span')[0].string

        # print(comment)
        return comment

    def start(self):
        print('开始抓取数据...')
        each = self._start
        while 1:
            url = 'http://lishi.tianqi.com/' + \
                self._city + '/' + str(each) + '.html'
            print(url)
            urlInfo = requests.get(
                url, cookies=self._cookies, headers=self._headers)
            print("从URL(%s)抓取评论中..." % urlInfo.url,)
            comment = self.crawlOnePage(urlInfo.text)
            comment['current'] = each
            self._tianqi.append(comment)
            if ('next' in comment):
                if(comment['next'] == self._end):
                    break
                time.sleep(round(random.uniform(3.0, 3.5), 2))
                each = comment['next']
            else:
                break
        self.save2csv()
        # self.fenci()

    def save2csv(self):
        self._fileName = 'weather_history_' + self._city + '.csv'
        print('保存到csv文件(%s)中...' % (self._fileName,))
        with open(os.path.join(sys.path[0], self._fileName), 'w', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['current', 'next', 'wind', 'temp', 'tianqi',
                          '紫外线指数', '旅游指数', '穿衣指数', '晾晒指数', '舒适度指数', '晨练指数']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(comment) for comment in self._tianqi]
        print('保存完毕...')

    def fenci(self):
        print('开始分词...')
        fenciFileName = os.path.join(
            sys.path[0], self._city + '_分词结果.csv')
        CommentRecord = namedtuple(
            'CommentRecord', ['user', 'date', 'eval', 'star', 'votes', 'content'])

        analyse.set_stop_words(os.path.join(sys.path[0], '中文停用词表.txt'))
        content = []
        csvName = os.path.join(sys.path[0], self._city + '.csv')
        for emp in map(CommentRecord._make, csv.reader(open(csvName, mode='r', encoding='utf-8-sig'))):
            content.append(emp.content)
        tags = analyse.extract_tags(
            ' '.join(content), topK=100, withWeight=True)
        with open(fenciFileName, 'w', encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            [writer.writerow([item[0], str(int(item[1] * 1000))])
             for item in tags]

        print('分词结束，保存结果在"%s"中...' % fenciFileName)


if __name__ == '__main__':

    defaults = {'start': '20170101', 'end': '20190501', 'city': 'xian'}
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city')
    parser.add_argument('-s', '--start')
    parser.add_argument('-e', '--end')
    namespace = parser.parse_args()
    command_line_args = {k: v for k, v in vars(namespace).items() if v}

    combined = ChainMap(command_line_args, defaults)

    TianqiHistoryCrawler(
        combined['city'], combined['start'], combined['end']).start()
