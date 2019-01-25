# Python步步飞升之豆瓣电影短评爬取，《白蛇：缘起》为啥这么热

## 1. 前言
一直喜欢动画电影，国内国外都看了不少。很让人欣慰的是，国产动画大电影已经长进不少，《魁拔》系列，《大圣归来》，《大护法》等都让我眼前一亮，最近正在上映的《白蛇：缘起》为追光动画出品，之前该公司的《小门神》就让我高兴的紧。在观影之前先看豆瓣评论以避深坑已经成为习惯，加之最近词图分析也很有意思，作次文抛砖引玉。

## 2. 大概思路

- 用BeautifulSoup从豆瓣电影上爬取短评保存文件中
- 从文件中找出评论内容用jieba分词
- 用在线可视化工具wordart生成热词图片

## 3. 从豆瓣电影上爬取短评

### 3.1 豆瓣网站爬虫限制

- 多次尝试之后发现，不登录的情况下，只能查询到200条短评
- 登录之后也只能查看500条短评
- 从豆瓣网站[robots.txt](https://www.douban.com/robots.txt)知道网站期望的被访问的间隔为5s
```
# Crawl-delay: 5
```

### 3.2 分析URL
刚开始进入短评url如下
```
https://movie.douban.com/subject/30331149/comments?start=0&limit=20&sort=new_score&status=P
```
查看源码搜索"后页"
```
<div id="paginator" class="center">
                <span class="first"><< 首页</span>
                <span class="prev">< 前页</span>
                <a href="?start=20&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="" class="next">后页 ></a>
        </div>
```
可以看到源码后页元素中有“start=20”，代码中获取这个start用以生成下一页待爬取url。
点击最下方“后页”按钮，新页面url如下
```
https://movie.douban.com/subject/30331149/comments?start=20&limit=20&sort=new_score&status=P
```
其中，**30331149**为《白蛇：缘起》电影id。每次下一页后，**start**+20，每页限制为20条数据。
因douban限制，短评最多能查看500条数据，所以进入url
```
https://movie.douban.com/subject/30331149/comments?start=480&limit=20&sort=new_score&status=P
```
之后发现“后页”按钮灰掉，已经不能再往下翻页了。
查看源码搜索"后页"
```
<div id="paginator" class="center">
                <a href="?start=0&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="1"><< 首页</a>
                <a href="?start=479&amp;limit=-20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page="">< 前页</a>
                <span class="next">后页 ></span>
        </div>
```
发现后页元素中start不存在，所以爬取的时候可以这点来判断是否结束爬取。
```
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
```

### 3.3 cookie模拟登录
最简单的方式就是在网站上登录之后，Chrome中“F12”快捷键点开调试工具，查看网络随意选取一个请求，记住header中cookie信息，爬取数据时添加到请求header。
![获取cookie](https://github.com/Kianhit/python-bbfeisheng/raw/master/crawler/result.png)
用requests发送请求时，带上cookie就好
```
self._cookies = {'cookie': cookie}
urlInfo = requests.get(url, cookies=self._cookies, headers=self._headers)
```

### 3.4 分析评论页源码获取指定信息
查看一个评论页面的源代码，发现
- 评论放在一个div中，id="comments"
- 每个评论都在一个div中，class="comment-item"
- 评论人名称在一个链接中，当href有值且链接中包含“people”元素，存在用户已注销情况
- 评论时间在一个span中，class="comment-time "
- 评论内容在一个span中，class="short"
- 评论打星在一个span中，class="rating"，存在未打分情况
- 投票在一个span中，class="votes"

用BS可以轻松提取这些数据，代码如下
```
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
```

### 4. 获取到的评论数据保存在csv中
使用csv模块可以很方便的保存文件
```
        fileName = self._movieName + '.csv'
        with open(fileName, 'w', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['user', 'date', 'eval', 'star', 'votes', 'content'] ## header
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            [writer.writerow(comment) for comment in self._comments] ## save comments line by line
```

### 5. 分词评论保存