# LyPycbr


擴充銀行

bcr/bank_demo.py

import bcr

class bank_bot(bcr.cls.bank):

    def __init__(self):  
        super().__init__('銀行名稱','爬蟲Url')
        
    def get_currrates(self):
        totalData = []
        c1 = bcr.cls.curr('TWD', '新台幣')
        c2 = bcr.cls.curr('TWD', '新台幣')
        r1 = bcr.cls.crate('現金',1,1)
        r2 = bcr.cls.crate('即期',1,1)
        cr1=self.createcurrrates(c1,c2,r1)
        cr2=self.createcurrrates(c1,c2,r2)
        totalData.append(cr1)
        totalData.append(cr2)
        return totalData
        
<p>bcr/__init__.py</p>

import bcr.bank_demo

bankrates =
[
        ......,
        bcr.bank_demo.bank_demo()
]


查詢新臺幣 vs 新加坡幣匯率

import bcr

ff=bcr.findRate('SGD')


TWD 新臺幣 vs SGD 新加坡幣

銀行       類型       買入匯率  賣出匯率 

台灣銀行   現金       21.72      22.5      
台灣銀行   即期       22.14      22.32     
台灣企銀   即期       22.1200    22.3000  
