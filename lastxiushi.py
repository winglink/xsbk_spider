# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import time
import os      #shell相关
import sys   
import Queue   #队列 
class XSBK:
    
        def __init__(self,url):
             self.baseurl=url
        def  getpage(self,url):
            try:
             user_agent ='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
             headers={'User-Agent':user_agent}
             request=urllib2.Request(url,headers=headers)
             result=urllib2.urlopen(request)
             return result
            except urllib2.URLError :
                 print 'failure connection'  
        def  sftime(self,tidata):
              
              timetu=time.localtime(tidata)
              curtime=time.strftime('%Y/%m/%d-%X',timetu)
              return curtime
        def  resolvedata(self,url):
               result=self.getpage(url)
               content=result.read().decode('utf-8')
               pattern=re.compile('<div.*?"author">.*?<img.*?>(.*?)</a>.*?'+
 '</div>.*?<div.*?"content">(.*?)<!--(\d+?)-->.{0,4}</div>(.*?)<i.*?"number">(\d+?)</i>',re.S)
               items=re.findall(pattern,content)   
               f=open('resultwing.txt','a')     
               for item in items:
                 item=list(item)
                 imagpa=re.compile('thumb')   #去除图片和视频
                 vediopa=re.compile('video_holder')
                 haveimg=re.search(imagpa,item[3])
                 havevedi=re.search(vediopa,item[3])
                 if haveimg or havevedi:
                         continue
                 item=[x.strip() for x in item] 
                 item[2]=self.sftime(float(item[2]))
  
                 print>>f,item[0].encode('utf-8')+'\n'+item[1].encode('utf-8')\
                 +'\n'+item[2].encode('utf-8')+'   '+item[4].encode('utf-8')
        def  nexturl(self,cuurl):     #获取该页面的其它链接
                 store=[]
                 result=self.getpage(cuurl)
                 content=result.read().decode('utf-8')
                 pattern=re.compile('<a.*?href="/(.*?)">.*?</a>',re.S)
                 
                 items=re.findall(pattern,content)
                 for item in items:
                       item=item.encode('utf-8')
                       if re.search(re.compile('page'),item):
                          store.append(self.baseurl+item)
                         # print item
                       if re.search(re.compile('hot'),item):
                           store.append(self.baseurl+item)
                          # print item
                       if re.search(re.compile('text',re.S),item) and not (re.search(re.compile('class',re.S),item)):
                           store.append(self.baseurl+item)
                          # print item
                 return store     
                             
                
                    
                 
                 
             
                 

def   start():
         os.system('touch resultwing.txt')
         baseurl='http://www.qiushibaike.com/'
         wing=XSBK(baseurl)
         #####
         #result=wing.getpage('http://www.qiushibaike.com/history" class="no_border" >穿越</a>')
        # print result.read()
         #return 0
         
         
         Urlqueue=Queue.Queue()
         Seen=set()
         Urlqueue.put(baseurl)
         Seen.add(baseurl)
         ####
        # wing.nexturl('http://www.qiushibaike.com/textnew')
        # return 0
         ######
         while (True):
            if Urlqueue.qsize()>0:
                print Urlqueue.qsize()
                currenturl=Urlqueue.get()  
                print currenturl            
                wing.resolvedata(currenturl) 
                for nexturl in  wing.nexturl(currenturl):
                     
                     if nexturl not in  Seen   :
                          Urlqueue.put(nexturl) 
                          Seen.add(nexturl)        
            else:
                       break
         print Seen              
         return 0               
              
        
         

             