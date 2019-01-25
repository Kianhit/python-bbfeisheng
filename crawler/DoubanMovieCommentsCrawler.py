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

'''
从豆瓣电影中抓取指定电影短评，然后保存于csv文件中
'''


class DoubanMovieCommentsCrawler(object):

    def __init__(self, movieId, cookie):
        self._movieId = str(movieId)
        self._movieName = ''
        self._comments = []
        self._cookies = {'cookie': cookie}
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}

    def crawlOnePage(self, html):
        soup = BeautifulSoup(html, 'lxml')
        # 获取电影名称
        if self._movieName == '':
            self._movieName = soup.select(
                '.movie-summary')[0].find_all('img')[0]['title']

        for item in soup.select('.comment'):
            comment = {}
            # 评论者
            for a in item.find_all('a'):
                if 'people' in a['href']:
                    comment['user'] = a.string
            # 日期
            comment['date'] = item.select('.comment-time')[0].string.strip()
            # 内容
            comment['content'] = item.select('.short')[0].string
            # 评价
            try:
                comment['eval'] = item.select('.rating')[0]['title']
                # stars
                comment['star'] = item.select('.rating')[0]['class'][0][-2]
            except Exception:
                # 存在用户没有打星情况
                # print(str(item).encode('GBK', 'ignore').decode('GBk'))
                comment['eval'] = '未打星'
                comment['star'] = '-1'
            # votes
            comment['votes'] = item.select('.votes')[0].string

            self._comments.append(comment)

        pages = re.findall(r'href="\?start=(\d+)&.+"',
                           str(soup.select('#paginator')))
        return pages

    def start(self):
        print('开始抓取数据...')
        each = 0
        while 1:
            url = 'https://movie.douban.com/subject/' + \
                self._movieId+'/comments?start=' + str(each) + \
                '&limit=20&sort=new_score&status=P'
            urlInfo = requests.get(
                url, cookies=self._cookies, headers=self._headers)
            print("从URL(%s)抓取评论中..." % urlInfo.url,)
            nextPage = self.crawlOnePage(urlInfo.text)
            # 没有下一页，最后一个元素为前页
            if int(nextPage[-1]) < each:
                print('抓取结束...')
                break
            else:
                time.sleep(round(random.uniform(5.0, 5.5), 2)) ## 随机暂停5-5.5s时间再发起请求
                each = int(nextPage[-1])
        self.save2csv()

    def save2csv(self):
        fileName = self._movieName + '.csv'
        print('保存到csv文件(%s)中...' % (fileName,))
        with open(fileName, 'w', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['user', 'date', 'eval', 'star', 'votes', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(comment) for comment in self._comments]
        print('保存完毕...')


if __name__ == '__main__':

    movieId=30331149

    # login douban.com
    cookie='__yadk_uid=HMbnanDUzuMuyxxj6S1fV6IMakVNThOz; \
        _vwo_uuid_v2=D1BEF4F661D8BBCF8BFB708C32CF59C8E|520c9e783d2c99bf3e33694e3146d731; \
        __utmv=30149280.236; ll="118318"; douban-fav-remind=1; \
        __utmz=30149280.1544958198.34.14.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; \
        __utmz=223695111.1544958198.29.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; \
        bid=3mDcL-drA-w; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1548313797%2C%22https%3A%2F%2F\
        www.baidu.com%2Flink%3Furl%3DW9OBUZ9tLE2gQ3bv-QW9ryJ7s1U9I5o45_N-JGFlbVBOfnNuZmGDl9RmheBAEIOk_IJMRFRk4D\
        yxmk5nf2HOWK%26wd%3D%26eqid%3D838ccf2b0004f360000000035c1630ed%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; \
        __utma=30149280.502717302.1516763713.1544958198.1548313798.35; __utmb=30149280.0.10.1548313798; \
        __utmc=30149280; __utma=223695111.1751593946.1517821407.1544958198.1548313798.30; \
        __utmb=223695111.0.10.1548313798; __utmc=223695111; dbcl2="2360219:e9Jnnva+QLk";\
         ck=uUEb; push_doumail_num=0; push_noty_num=0; _pk_id.100001.4cf6=8cba87048d36e6b1.1517821407.29.1548313934.1544958651.'

    defaults={'id': movieId, 'cookie': cookie}
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--id')
    parser.add_argument('-c', '--cookie')
    namespace=parser.parse_args()
    command_line_args={k: v for k, v in vars(namespace).items() if v}

    combined=ChainMap(command_line_args, defaults)

    DoubanMovieCommentsCrawler(combined['id'], combined['cookie']).start()
