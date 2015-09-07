# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os
import sys

from sinaBlogContentTool import sinaBlogContentTool

reload(sys)
sys.setdefaultencoding('utf-8')

class Spider:
    '''
    功能：用于下载sina博客内容。
    初始输入：类别为“全部博文”的页面URL
            自动解析页面，获取所有类别
            用户可按照分类类别来下载博客内容
    最终结果：博文文字+图片均保存到本地，为markdown格式文件
    '''
    def __init__(self, indexUrl):
        print 'Spider'
        self.indexUrl = indexUrl
        content = indexUrl.split('/')[-1].split('_')
        self.userID = content[1]
        self.defaultPage = self.getPage(self.indexUrl)
        
    def getPage(self, indexUrl):
        '''获取indexUrl页面'''
        request = urllib2.Request(indexUrl)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')
    
    def getPageNum(self,page):
        '''计算有几页博客目录'''
        pattern = re.compile('<li class="SG_pgnext">', re.S)
        result = re.search(pattern, page)
        if result:
            print u"目录有多页，正在计算……"
            pattern2 = re.compile(u'<li class="SG_pgnext">.*?>共(.*?)页', re.S)
            num = re.search(pattern2, page)
            pageNum = str(num.group(1))
            print u"共有", pageNum, u"页"
        else:
            print u"只有1页目录"
            pageNum = 1
        return int(pageNum)
    
    def getTypeNum(self):
        '''计算有几种分类'''
        pattern = re.compile('<span class="SG_dot">.*?<a href="(.*?)".*?>(.*?)</a>.*?<em>(.*?)</em>', re.S)
        result = re.findall(pattern, self.defaultPage)
        pattern2 = re.compile(u'<strong>全部博文</strong>.*?<em>(.*?)</em>', re.S)
        result2 = re.search(pattern2, self.defaultPage)
        self.allType = {}
        i = 0
        self.allType[i] = (self.indexUrl, u"全部博文", result2.group(1)[1:-1])
        for item in result:
            i += 1
            self.allType[i] = (item[0], item[1], item[2][1:-1])
        print u"本博客共有以下", len(self.allType), "种分类："
        for i in range(len(self.allType)):
            print "ID: %-2d  Type: %-30s Qty: %s" % (i, self.allType[i][1], self.allType[i][2])
#             , self.allType[i][0]
    
    def getBlogList(self,page):
        '''获取一页内的博客URL列表'''
        pattern = re.compile('<div class="articleCell SG_j_linedot1">.*?<a title="" target="_blank" href="(.*?)">(.*?)</a>', re.S)
        result = re.findall(pattern, page)
        blogList = []
        for item in result:
            blogList.append((item[0], item[1].replace('&nbsp;', ' ')))
        return blogList
    
    def mkdir(self,path):
        isExist = os.path.exists(path)
        if isExist:
            print u"名为", path, u"的文件夹已经存在"
            return False
        else:
            print u"正在创建名为", path, u"的文件夹"
            os.makedirs(path)
    
    def saveBlogContent(self,path,url):
        '''保存url指向的博客内容'''
        page = self.getPage(url)
        blogTool = sinaBlogContentTool(page)
        blogTool.parse()
        
        filename =  path + '/' + blogTool.time + '  ' + blogTool.title.replace('/', u'斜杠') + '.markdown'
        with open(filename, 'w+') as f:
            f.write("URL: "+url)
            f.write("标签：")
            for item in blogTool.tags:
                f.write(item.encode('utf-8'))
                f.write(' ')
            f.write('\n')
            f.write("类别：")
            f.write(blogTool.types.encode('utf-8'))
            f.write('\n')
            picNum = 0
            for item in blogTool.contents:
                if item[0] == 'txt':
                    f.write('\n')
                    f.write(item[1].encode('utf-8'))
                elif item[0] == 'img':
                    f.write('\n')
                    f.write('!['+ str(picNum) + '](' + item[1] + ')')
                    picNum += 1
        
        print u"下载成功"
    
    def getBlogName(self,page):
        '''获取博客名字，暂未调用'''
        pattern = re.compile('<span id="blognamespan">(.*?)</span>', re.S)
        result = re.search(pattern, page)
        print result.group(1)
        return result.group(1)
    
    def run(self):
        self.getTypeNum()
        i = raw_input(u"请输入需要下载的类别ID(如需要下载类别为“全部博文”类别请输入0):")
        page0 = self.getPage(self.allType[int(i)][0])
        pageNum = self.getPageNum(page0)
        urlHead = self.allType[int(i)][0][:-6]
        typeName = self.allType[int(i)][1]
        typeBlogNum = self.allType[int(i)][2]
        if typeBlogNum == '0':
            print u"该目录为空"
            return
        self.mkdir(typeName)
        for j in range(pageNum):
            print u"------------------------------------------正在下载类别为", typeName, u"的博客的第", str(j+1), u"页------------------------------------------"
            url = urlHead + str(j+1) + '.html'
            page = self.getPage(url)
            blogList = self.getBlogList(page)
            print u"本页共有博客", len(blogList), u"篇"
            for item in blogList:
                print u"正在下载博客《", item[1], u"》中……"
                self.saveBlogContent(typeName, item[0])
        print u"全部下载完毕"
        
if __name__ == '__main__':
    indexUrl = sys.argv[1]
#     indexUrl = 'http://blog.sina.com.cn/s/articlelist_1215172700_0_1.html'
#     indexUrl = 'http://blog.sina.com.cn/s/articlelist_1640571365_0_1.html'
    spider = Spider(indexUrl)
#     spider.getBlogName(spider.defaultPage)
#     print spider.getPage(indexUrl)
#     spider.getPageNum()
#     spider.getIndexPageUrl(0, 2)
#     spider.getTypeNum()
    spider.run()