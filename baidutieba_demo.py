#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
 
#百度贴吧爬虫类
class BDTB:
 
    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.formatTool = FormatTool()
 
    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None

    def getContent(self,pageNum):

    	page = self.getPage(pageNum).read()
    	pattern = re.compile('<div.*?post_content ">(.*?)</div>',re.S)
    	items = re.findall(pattern,page)
    	
    	pageContent = ""

    	for item in items:
    		item = self.formatTool.replace(item)
    		pageContent = pageContent + item+ "\n"

    	return pageContent
   
class FormatTool:

	def __init__(self):

		self.removeIMG = re.compile('<img.*?>',re.S)
		self.removeBR = re.compile('<br>',re.S)
		self.removeBP = re.compile(' {7}',re.S)
		self.removeLink = re.compile('<a.*?>.*?</a>',re.S)

	def replace(self,content):

		content = re.sub(self.removeIMG,"",content)
		content = re.sub(self.removeLink,"",content)
		content = re.sub(self.removeBR,"\n",content)
		content = re.sub(self.removeBP,"",content)

		return content.strip()
 
if __name__ == '__main__':

	baseURL = 'http://tieba.baidu.com/p/3138733512'
	bdtb = BDTB(baseURL,1)
	content = ""
	for i in range(5):
		content = content + bdtb.getContent(i+1)
	print "Content is saved in file..."

	file = open("tb.txt","w")
	file.write(content)
