# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re

class stu:
    def __init__(self):
        self.loginurl = 'http://zhjw.scu.edu.cn/loginAction.do' #登录路径
        self.gradurl = 'http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo' #成绩路径
        self.cookies = cookielib.CookieJar() #保存cookies
        self.postdata = urllib.urlencode({
            'zjh':'', #student ID
            'mm':'' #password
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self.credit = []
        self.grades = []

    def getPage(self):
        req = urllib2.Request(
            url = self.loginurl,
            data = self.postdata)
        res = self.opener.open(req) #登录
        res = self.opener.open(self.gradurl) #进入成绩页面
        return res.read().decode('GBK')

    def getGrades(self):
        page = self.getPage()
        print(page)
        #正则：取出分数
        mygrade = re.findall('<tr.*?<td.*?<td.*?<td.*?<td.*?<td.*?>\r\n(.*?)</td>.*?<td.*?<td.*?<p.*?>(.*?)&.*?</p>.*?</tr>', page, re.S|re.M|re.I)
        #正则：取出学分
        mycredit = re.findall(
            '<tr.*?<td.*?<td.*?<td.*?<td.*?<td.*?>\r\n(.*?)\r\n.*?</td>.*?<td.*?<td.*?<p.*?>(.*?)&.*?</p>.*?</tr>', page,
            re.S | re.M | re.I)
        #正则获得的学分和分数格式规范化（可以通过写出更好正则来解决
        for i in mygrade:
            self.grades.append(i[1].encode('GBK'))
        for i in mycredit:
            for j in i[0]:
                if j<='9' and j>='0' :
                    self.credit.append(j.encode('GBK'))
        self.getgrad()

    def getgrad(self):
        sum = 0
        w = 0
        for i in range(len(self.credit)):
            #跳过非数字的成绩
            try:
                self.grades[i]=float(self.grades[i])
                self.credit[i]=float(self.grades[i])
                sum += self.credit[i] * self.grades[i]
                w += self.credit[i]
            except:
                continue
        print(sum/w)


s = stu()
s.getGrades()

#'zjh':'2014141463166',
#'mm':'290242'