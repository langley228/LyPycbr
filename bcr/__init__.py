
import bcr.cls
import bcr.bank_bot
import bcr.bank_tbb

currcode=bcr.cls.currlist()

bankrates=[
        bcr.bank_bot.bank_bot(),
        bcr.bank_tbb.bank_tbb()
]

def findRate(curr2,curr1='TWD'):
    print("{c1} vs {c2}".format(c1=currcode.findCurr(curr1) ,c2=currcode.findCurr(curr2)))
    print("{bank:8} {t:8} {b:5} {s:5}".format(bank='銀行' ,t='類型',b='買入匯率',s='賣出匯率'))
    for bk in bankrates:
        listx=bk.findRate(curr2,curr1)
        for a in listx:
            print("{bank:6} {t:8} {b:10} {s:10}".format(bank=bk.name ,t=a.rate.rtype,b=a.rate.buy,s=a.rate.sell))

def printcurrs():    
    print(bcr.currcode)