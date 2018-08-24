# -*- coding: utf-8 -*-
# @Time    : 2018/08/01
# @Author  : PanDong
# @Software: PyCharm





import os
from TimeParse import TimeParse


text='''
    10：20-16：30
    每3个月休一次假期
    2019年3月7日至2019年4月1日
    1993年植树节
    小明在7月六号早上8点买了瓶1982年9月生产的雷碧
    上课时间为7-9月份
    2020年元旦快乐！！
'''

t=TimeParse()
outcome=t.tipa(text)
print(outcome)




# with open("test.txt","r",encoding='utf-8') as w:
#     text=w.read()
#
# t=TimeParse()
# outcome=t.tipa(text)
#
# with open("outcome.txt","w",encoding='utf-8') as f:
#     f.write(outcome)
