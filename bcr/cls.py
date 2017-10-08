# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 22:01:06 2017

@author: Langley
"""
import abc
import requests
from bs4 import BeautifulSoup 
import bcr

class curr(object):
    def __init__(self, code, name):
        self.__code = code
        self.__name = name
        
    def __str__(self):
        return "{code} {name}".format(code=self.code, name=self.name)
        
    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value


class crate(object):
    def __init__(self, rtype, buy, sell):
        self.__rtype = rtype
        self.__buy = buy  
        self.__sell = sell  
        
    def __str__(self):
        return "{rtype} B:{buy} S:{sell}".format(rtype=self.rtype, buy=self.buy, sell=self.sell)
    
    @property
    def rtype(self):
        return self.__rtype
    @rtype.setter
    def rtype(self, value):
        self.__rtype = value
        
    @property
    def buy(self):
        return self.__buy
    @buy.setter
    def buy(self, value):
        self.__buy = value
        
    @property
    def sell(self):
        return self.__sell
    @sell.setter
    def sell(self, value):
        self.__sell = value        
        
class currrate(object):
    def __init__(self, acurr):
        self.__curr1 = curr(acurr.code, acurr.name)
        self.__curr2 = curr(acurr.code, acurr.name)
        self.__rate = crate('現金匯率', 1, 1)
            
    def __str__(self):
        return "{curr1} {curr2} {rate}".format(curr1=self.curr1, curr2=self.curr2, rate=self.rate)
    
    @property
    def curr1(self):
        return self.__curr1

    @curr1.setter
    def curr1(self, value):
        self.__curr1 = value
        
    @property
    def curr2(self):
        return self.__curr2

    @curr2.setter
    def curr2(self, value):
        self.__curr2 = value        
        
    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, value):
        self.__rate = value  
        
class currlist(object):
    def __init__(self):
        self.__currs = self.__getCurrs()
        
    def __str__(self):
        s=''
        for c in self.__currs:
            if s!='':s+='\r\n'
            s+=c.__str__()
        return s
    
    
    def __getCurrs(self):
        # 向台灣銀行網站拿匯率資料
        rate = requests.get("https://developers.google.com/adsense/host/appendix/currencies?hl=zh-tw")
        # 利用BeautifulSoup整理資料，並使用html parser
        rate_soup=BeautifulSoup(rate.text,'html.parser')
        # 找到表格，拿出tbody中所有的tr
        rows = rate_soup.find('table').find_all('tr')
        # 待會處理完的所有資料，要放在totalData這個list
        totalData = []
        # 巡訪每一個tr
        for row in rows:
           # 將每個td處理完的內容暫存於currentTDlist中
           currentTDlist = []
           # 巡訪每一個td
           for eachTD in row:
               # 根據網頁發現，外幣名稱要好幾層才解析的到，所以當拿不到時，用另一種方法去找到它
               # 也觀察到外幣名稱是放在一個類別為visible-phone的div元件中
               # strip()可以把字串前後的空白移除
               if eachTD.string is None:
                   currentTDlist.append(eachTD.find("div", class_='visible-phone').string.strip())
               # 處理網頁時會跑出很多換行符號，所以也忽略不計，不是換行的才留下
               elif eachTD.string != '\n':
                   currentTDlist.append(eachTD.string)
               else:
                   continue
           c1 = curr(currentTDlist[0], currentTDlist[1])
           totalData.append(c1)
        
        # 印出美金的賣出現金匯率
        return totalData   
    @property
    def value(self):
        return self.__currs
    
    def findCurr(self,code):
        for c in self.__currs:
            if c.code==code:
                return c
        return None
        
class bank(metaclass=abc.ABCMeta):
    def __init__(self, name, url):
        self.__name = name
        self.__url = url
        self.__currlist = bcr.currcode.value
        self.__currrates = self.get_currrates()
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value
        
    @property
    def currrates(self):
        return self.__currrates
    
    @abc.abstractstaticmethod
    def get_currrates(self):
        pass          
    
    def createcurrrates(self,curr1,curr2,crate):
        x=currrate(self.__fixCurr(curr1))
        x.curr2=self.__fixCurr(curr2)
        x.rate=crate
        return x
        
    def __fixCurr(self,curr):
        for c in self.__currlist:
            if c.code==curr.code:
                return c
            elif c.name==curr.name:
                return c
        return curr
            
    
    def findRate(self,curr2,curr1='TWD'):
        r=[]
        for b in self.__currrates:
            if b.curr1.code==curr1 and b.curr2.code==curr2:
                r.append(b)
        return r
            