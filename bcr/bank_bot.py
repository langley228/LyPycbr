# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 22:02:11 2017

@author: Langley
"""
import bcr
import requests
from bs4 import BeautifulSoup 

class bank_bot(bcr.cls.bank):
    def __init__(self):  
        super().__init__('台灣銀行','http://rate.bot.com.tw/xrt?Lang=zh-TW')
        
    def get_currrates(self):
        # 向台灣銀行網站拿匯率資料
        rate = requests.get(self.url)
        # 利用BeautifulSoup整理資料，並使用html parser
        rate_soup=BeautifulSoup(rate.text,'html.parser')
        # 找到表格，拿出tbody中所有的tr
        rows = rate_soup.find('table','table').tbody.find_all('tr')
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
           c1 = bcr.cls.curr('TWD', '新台幣')
           c2 = bcr.cls.curr('TWD', '新台幣')
           c2.name=currentTDlist[0]
           c2.code=c2.name[c2.name.index('(')+1:c2.name.index(')')]
           c2.name=c2.name[:c2.name.index('(')]
           c2.name=c2.name.replace(' ','')
           r1 = bcr.cls.crate('現金',currentTDlist[1],currentTDlist[2])
           r2 = bcr.cls.crate('即期',currentTDlist[3],currentTDlist[4])
           cr1=self.createcurrrates( c1,c2,r1)
           cr2=self.createcurrrates( c1,c2,r2)
           
           #print(cr1)
           #print(cr2)
           #print(currentTDlist)
           #totalData.append(currentTDlist)
           totalData.append(cr1)
           totalData.append(cr2)
        
        # 印出美金的賣出現金匯率
        #print(totalData[0][2])
        return totalData