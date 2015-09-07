# -*- coding:utf-8 -*-

import re
import urllib2
from bs4 import BeautifulSoup
import string
from bs4.element import NavigableString

class sinaBlogContentTool:
    def __init__(self,page):
        self.page = page
    
    def parse(self):
        '''解析博客内容'''
        soup = BeautifulSoup(self.page)
        
        self.title = soup.body.find(attrs = {'class':'titName SG_txta'}).string
        
        self.time = soup.body.find(attrs = {'class':'time SG_txtc'}).string
        self.time = self.time[1:-1]
        print u"发表日期是：", self.time, u"博客题目是：", self.title
        
        self.tags = []
        for item in soup.body.find(attrs = {'class' : 'blog_tag'}).find_all('h3'):
            self.tags.append(item.string)
        
        self.types = u"未分类"
        if soup.body.find(attrs = {'class' : 'blog_class'}).a:
            self.types = soup.body.find(attrs = {'class' : 'blog_class'}).a.string

        self.contents = []
        self.rawContent = soup.body.find(attrs = {'id' : 'sina_keyword_ad_area2'})

        for child in self.rawContent.children:
            if type(child) == NavigableString:
                self.contents.append(('txt', child.strip()))
            else:
                for item in child.stripped_strings:
                    self.contents.append(('txt', item))
                if child.find_all('img'):
                    for item in child.find_all('img'):
                        if(item.has_attr('real_src')):
                            self.contents.append(('img', item['real_src']))



if __name__ == '__main__':
    print "main"
    url = 'http://blog.sina.com.cn/s/blog_486e105c01000crv.html'
#     url = 'http://blog.sina.com.cn/s/blog_486e105c0100ar8b.html'
#     url = 'http://blog.sina.com.cn/s/blog_61c921e50102viur.html'
#     url = 'http://blog.sina.com.cn/s/blog_59a7d1980102vrvx.html'
    page = urllib2.urlopen(url).read().decode('utf-8')
    blogTool = sinaBlogContentTool(page)
    blogTool.parse()
    