import re
import os
from TimeReg import TimeReg




class TimeRecognition:
    '''时间识别类'''

    def __init__(self):
        pass

    def recognition(self,text):
        t = TimeReg()
        answer = re.finditer(t.time_reg,text)
        spans = []
        contents = []

        for i in answer:
            spans.append(i.span())
            contents.append(i.group())

        contents = [i for i in contents if i != '']
        spans = [i for i in spans if i[0] != i[1]]  # 去掉识别结果为空的位置信息


        return contents,spans   #返回识别出的内容和位置跨度



if __name__ == "__main__":
    pass