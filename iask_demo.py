#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import pdb

class IASKSpider:
 
    #初始化，传入基地址和开始页
    def __init__(self,baseUrl,startPage,endNum):

        self.baseURL = baseUrl
        self.startPage = startPage
        self.formatTool = FormatTool()
   
        self.endNum = endNum
        self.file = open("iask_question_and_answer.txt",'w+')

    #传入url，获取该页的代码
    def getPage(self,pageStr):

        try:
            url = self.baseURL + pageStr
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接新浪爱问失败,错误原因",e.reason
                return None

    def getContent(self):

    	#获得起始页的源码
    	
    	#page = self.getPage(self.startPage).read().decode("utf-8")
    	page = self.getPage(self.startPage).read()
    	#pdb.set_trace()

    	#获得1-100页的源码
    	for i in range(1,self.endNum):
    		print ("正在获得第%d页的源码..." %(i))
    		self.file.write("第%d页的问题\n" %(i))
    		#解析当前页源码
    		soup = BeautifulSoup(page,"lxml")
    		#获得当前页的地址
    		current = soup.find("a", string=i)
    		#获得当前页的问题
    		questions = soup.find_all('div', class_='question-title')
    		#处理当前页的问题
    		print ("正在处理第%d页的问题..." %(i))
    		self.handleQuestions(questions)
    		
    		#处理完当前页，跳到下一页
    		page = self.getPage(current['href']).read()
    		
    	self.file.close()

    def handleQuestions(self,questions):

    	#处理questions中的每一个question
    	for question in questions:
    			for a in question.children:
    				aString = str(a).strip()
    				pattern = re.compile('<a href="(.*?)".*?>(.*?)</a>',re.S)
    				check = re.search(pattern,aString)
    				if check:
    					items = re.findall(pattern,aString)
    					#获得问题详情链接和问题内容
    					item = items[0]
    					href = item[0]
    					questionStr = item[1]
    					
    					ansPage = self.getPage(href).read()
    					ansStr = self.getAnswer(ansPage)

    					self.file.write("Q:"+questionStr+"\n")
    					self.file.write("A:"+ansStr+"\n\n")
    				

    def getAnswer(self,page):
    	pattern = re.compile('<div class="good_answer.*?<div>.*?<span>(.*?)</span>',re.S)
    	check = re.search(pattern,page)
    	ansStr = ''
    	if check:
    		items = re.findall(pattern,page)
    		ansStr = self.formatTool.replace(items[0])
    	
    	return ansStr

   
class FormatTool:

	def __init__(self):

		self.removeIMG = re.compile('<img.*?>',re.S)
		self.removeBR = re.compile('<br>|<br/>',re.S)
		self.removeBP = re.compile(' {7}',re.S)
		self.removeLink = re.compile('<a.*?>.*?</a>',re.S)
		self.removeDIV = re.compile('<div.*?>.*?</div>',re.S)
		self.removePre1 = re.compile('<pre>',re.S)
		self.removePre2 = re.compile('</pre>',re.S)

	def replace(self,content):

		content = re.sub(self.removeBR,"\n",content)
		content = re.sub(self.removeLink,"",content)
		content = re.sub(self.removeDIV,"",content)
		content = re.sub(self.removePre1,"",content)
		content = re.sub(self.removePre2,"",content)

		return content.strip()
 
if __name__ == '__main__':

	baseURL = 'http://iask.sina.com.cn'
	startPage = '/c/74-all-1-new.html'
	iaskSpider = IASKSpider(baseURL,startPage,101)
	iaskSpider.getContent()
	
