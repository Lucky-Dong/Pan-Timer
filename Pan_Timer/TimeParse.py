# -*- coding: utf-8 -*-
# @Time    : 2018/08/01
# @Author  : PanDong
# @Software: PyCharm


import re
import os
from TimeRecognition import TimeRecognition
from TimeFunction import *
from TriggerWord import TriggerWord
from datetime import timedelta, datetime
import datetime


class TimeParse:
    def __init__(self):
        pass

    def tipa(self, text):
        '''
        时间归一化方法
        :param text:
        :return:
        '''

        t = TimeRecognition()
        contents, spans = t.recognition(text)

        list_text = list(text)
        increment = 0

        # ------------------------------------------------------------------------------------------------------------
        for index in range(0, len(contents)):

            flag = 0
            content = contents[index]

            for i in TriggerWord.fuzzy:  # 模糊时间 刚刚
                if i in content:
                    list_text.insert(spans[index][0] + increment, '<TIME,FUZZY>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1
                    break
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            for i in TriggerWord.settime:  # 循环时间 每两天
                if i in content:
                    src = ""  # 记录临时数字
                    for j in range(len(content)):
                        if content[j] in TriggerWord.TIME_NUM:
                            src += content[j]
                        if content[j] in TriggerWord.set_unit.keys():
                            time_uni = TriggerWord.set_unit[content[j]]

                    if src == "":
                        src = 1
                    else:
                        src = cn2dig(src)
                    if src != None and time_uni != None:
                        list_text.insert(spans[index][0] + increment, '<TIME,SET,E' + str(src) + time_uni + '>')
                        increment += 1
                        list_text.insert(spans[index][1] + increment, '</TIME>')
                        increment += 1
                        flag = 1
                        break
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            if '-' in content:
                if re.match(r'\d{4}-(\d{1,2})-(\d{1,2})', content) != None:  # 点时间 2013-1-19
                    list_text.insert(spans[index][0] + increment, '<TIME,DATE,' + content + 'T00:00:00' + '>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1

                elif re.search(r'(\d{1,2})[:：](\d{1,2})-(\d{1,2})[:：](\d{1,2})', content) != None:  # 9:10-13:20

                    ans = re.search(r'(\d{1,2})[:：](\d{1,2})-(\d{1,2})[:：](\d{1,2})', content)
                    h1 = ans.group(1)
                    m1 = ans.group(2)
                    h2 = ans.group(3)
                    m2 = ans.group(4)

                    first = timedelta(minutes=int(m1), hours=int(h1))
                    last = timedelta(minutes=int(m2), hours=int(h2))
                    howlong = last - first
                    src = howlong.seconds
                    src = src // 60
                    list_text.insert(spans[index][0] + increment, '<TIME,DURATION,' + str(src) + 'm>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1

                elif re.search(
                        r'(?:[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+\w)?([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)-([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)(?!:)(\w+)',
                        content) != None:
                    ans = re.search(
                        r'(?:[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+\w)?([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)-([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)(?!:)(\w+)',
                        content)  # 和'-'相关的段时间
                    g1 = ans.group(1)
                    g2 = ans.group(2)
                    g3 = ans.group(3)
                    g1 = cn2dig(g1)
                    g2 = cn2dig(g2)
                    src = g2 - g1
                    for i in range(len(g3)):
                        if g3[i] in TriggerWord.set_unit.keys():
                            time_uni = TriggerWord.set_unit[g3[i]]
                            break
                        else:
                            time_uni = "D"

                    if src != None and time_uni != None:
                        list_text.insert(spans[index][0] + increment, '<TIME,DURATION,' + str(src) + time_uni + '>')
                        increment += 1
                        list_text.insert(spans[index][1] + increment, '</TIME>')
                        increment += 1
                        flag = 1

            if flag != 0:
                continue
            # ------------------------------------------------------------------------------------------------------------
            if "内" in content:  # 关于"内"的段时间
                src = ""
                for j in range(len(content)):
                    if content[j] in TriggerWord.TIME_NUM:
                        src += content[j]
                    if content[j] in TriggerWord.set_unit.keys():
                        time_uni = TriggerWord.set_unit[content[j]]
                if src != None:
                    src = cn2dig(src)
                    list_text.insert(spans[index][0] + increment, '<TIME,DURATION,' + str(src) + time_uni + '>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            if re.match(r'半[个]?[多]?小时', content) != None:
                ans = re.match(r'半[个]?[多]?小时', content)

                list_text.insert(spans[index][0] + increment, '<TIME,DURATION,30m>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            if "个" in content:
                src = ""
                for j in range(len(content)):
                    if content[j] in TriggerWord.TIME_NUM:
                        src += content[j]
                    if content[j] in TriggerWord.set_unit.keys():
                        time_uni = TriggerWord.set_unit[content[j]]
                    else:
                        time_uni = "M"

                if src != None:
                    src = cn2dig(src)
                    list_text.insert(spans[index][0] + increment, '<TIME,DURATION,' + str(src) + time_uni + '>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1
            if flag != 0:
                continue
            # ------------------------------------------------------------------------------------------------------------
            if re.search(r'^\d+[天月日周年]$', content) != None:  # 30天
                ans = re.search(r'(\d+)([天月日周年])', content)
                g1 = ans.group(1)
                g2 = ans.group(2)
                if g2 in TriggerWord.set_unit.keys():
                    time_uni = TriggerWord.set_unit[g2]
                    list_text.insert(spans[index][0] + increment, '<TIME,DURATION,' + g1 + time_uni + '>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            if re.match(r'([上下中]午|晚[上]?|早[上]?|凌晨)?(\d{1,2})[:：](\d{1,2})[分]?', content) != None:  # 30天
                ans = re.search(r'([上下中]午|晚[上]?|早[上]?|凌晨)?(\d{1,2})[:：](\d{1,2})[分]?', content)
                afternoon = ans.group(1)
                g1 = ans.group(2)
                g2 = ans.group(3)
                if afternoon in ["下午", "晚", "晚上"]:
                    if int(g1) < 12:
                        g1 = int(g1) + 12
                list_text.insert(spans[index][0] + increment, '<TIME,DATE,0000-00-00T' + str(g1) + ':' + g2 + ":" + '>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------

            if "至" in content:  # 自2015年4月15日起至2015年4月21日止
                pass
                # src=""
                #
                # for j in range(len(content)):
                #     if content[j] in TriggerWord.TIME_NUM:
                #         src += content[j]
                #     if content[j] in TriggerWord.set_unit.keys():
                #         time_uni = TriggerWord.set_unit[content[j]]

            # ------------------------------------------------------------------------------------------------------------

            if re.search(r'\d{4}\.\d{1,2}\.\d{1,2}', content) != None:  # 2013.2.12

                ans = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', content)
                g1 = ans.group(1)
                g2 = ans.group(2)
                g3 = ans.group(3)
                list_text.insert(spans[index][0] + increment, '<TIME,DATE,' + g1 + '-' + g2 + '-' + g3 + 'T00:00:00>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1

            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------
            if re.match(r'^(\d{4})$', content) != None:  # [2013]
                ans = re.search(r'^(\d{4})$', content)
                g1 = ans.group(1)
                list_text.insert(spans[index][0] + increment, '<TIME,DATE,' + str(g1) + '-00-00T00:00:00>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1

            if flag != 0:
                continue

            # -----------------------------------------------------------------------------------------------------------
            if re.match(
                    r'[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号]([凌早]晨|[傍夜]晚|[早晚]上|[上中下]午)?\w{1,2}[时点:：]\w{1,2}[分]?',
                    content) != None:
                ans = re.search(
                    r'([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+)年(\w{1,2})月([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2})[日号]([凌早]晨|[傍夜]晚|[早晚]上|[上中下]午)?(\w{1,2})[时点:：](\w{1,2})[分]?',
                    content)
                afternoon = ans.group(4)
                g1 = year2dig(ans.group(1))
                g2 = cn2dig(ans.group(2))
                g3 = cn2dig(ans.group(3))
                g5 = cn2dig(ans.group(5))
                g6 = cn2dig(ans.group(6))

                if afternoon in ["下午", "晚", "晚上"]:
                    if int(g5) < 12:
                        g5 = int(g5) + 12
                list_text.insert(spans[index][0] + increment, '<TIME,DATE,' + str(g1) + '-'+str(g2)+'-'+str(g3)+'T'+str(g5)+':' + str(g6)  + '>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------

            if re.search(r'([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+年)?(植树节|圣诞节|青年节|教师节|儿童节|元旦|国庆|劳动节|妇女节|建军节|航海日节|建党节|记者节)',
                         content) != None:
                ans = re.search(
                    r'([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+年)?(植树节|圣诞节|青年节|教师节|儿童节|元旦|国庆|劳动节|妇女节|建军节|航海日节|建党节|记者节)',
                    content)
                year = '0000'
                if ans.group(1) != None:
                    year1 = ans.group(1)
                    year1 = year1[:-1]
                    year = cn2dig(year1)

                m = ans.group(2)
                month = TriggerWord.holi_solar[m]

                list_text.insert(spans[index][0] + increment,
                                 '<TIME,DATE,' + str(year) + '-' + str(month) + 'T00:00:00>')
                increment += 1
                list_text.insert(spans[index][1] + increment, '</TIME>')
                increment += 1
                flag = 1
            if flag != 0:
                continue

            # ------------------------------------------------------------------------------------------------------------

            if flag == 0:
                src = ""
                t_unit = {
                    "year": [],
                    "month": [],
                    "day": [],
                    "hour": [],
                    "minute": [],
                }
                duration_flag = 0  # 判断点时间 段时间
                for j in range(len(content)):

                    if content[j] in TriggerWord.TIME_NUM:
                        src += content[j]
                    elif content[j] in TriggerWord.set_unit.keys():
                        time_uni = TriggerWord.set_unit[content[j]]
                        if time_uni == "Y":
                            src = year2dig(src)
                            t_unit["year"].append(src)
                            src = ""
                            continue

                        if time_uni == "M":
                            src = cn2dig(src)
                            t_unit["month"].append(src)
                            src = ""
                            continue

                        if time_uni == "D":
                            src = cn2dig(src)
                            t_unit["day"].append(src)
                            src = ""
                            continue

                        if time_uni == "h":
                            src = cn2dig(src)
                            t_unit["hour"].append(src)
                            src = ""
                            continue

                        if time_uni == "m":
                            src = cn2dig(src)
                            t_unit["minute"].append(src)
                            src = ""
                            continue

                for key, value in t_unit.items():
                    if key == "day":
                        if len(value) == 1:
                            day1 = value[0]
                            day2 = value[0]
                        elif len(value) == 2:
                            day1 = value[0]
                            day2 = value[1]
                            duration_flag = 1
                        else:
                            day1 = 0
                            day2 = 0

                    elif key == "hour":
                        if len(value) == 1:
                            hour1 = value[0]
                            hour2 = value[0]
                        elif len(value) == 2:
                            hour1 = value[0]
                            hour2 = value[1]
                            duration_flag = 1
                        else:
                            hour1 = 0
                            hour2 = 0

                    elif key == "minute":
                        if len(value) == 1:
                            minute1 = value[0]
                            minute2 = value[0]
                        elif len(value) == 2:
                            minute1 = value[0]
                            minute2 = value[1]
                            duration_flag = 1
                        else:
                            minute1 = 0
                            minute2 = 0

                    elif key == "year":
                        if len(value) == 1:
                            year1 = value[0]
                            year2 = value[0]
                        elif len(value) == 2:
                            year1 = value[0]
                            year2 = value[1]
                            duration_flag = 1
                        else:
                            year1 = 0
                            year2 = 0


                    elif key == "month":
                        if len(value) == 1:
                            month1 = value[0]
                            month2 = value[0]
                        elif len(value) == 2:
                            month1 = value[0]
                            month2 = value[1]
                            duration_flag = 1
                        else:
                            month1 = 0
                            month2 = 0

                if duration_flag == 1:

                    first = timedelta(minutes=int(minute1), hours=int(hour1))
                    last = timedelta(minutes=int(minute2), hours=int(hour2))
                    t_long = last - first

                    src = t_long.seconds
                    src = src // 60
                    minute_src = src
                    d_u = "m"

                    if year1 == 0:
                        year1 += 1
                    if year2 == 0:
                        year2 += 1
                    if month1 == 0:
                        month1 += 1
                    if month2 == 0:
                        month2 += 1
                    if day1 == 0:
                        day1 += 1
                    if day2 == 0:
                        day2 += 1

                    d1 = datetime.date(year1, month1, day1)
                    d2 = datetime.date(year2, month2, day2)
                    d_long = d2 - d1
                    day_src = d_long.days

                    # except:
                    #     day_src=0
                    #     print("ssssssss" + str(day_src))



                else:
                    if t_unit["year"] == []:
                        t_unit["year"].append("0000")

                    if t_unit["month"] == []:
                        t_unit["month"].append("00")

                    if t_unit["day"] == []:
                        t_unit["day"].append("00")

                    if t_unit["hour"] == []:
                        t_unit["hour"].append("00")

                    if t_unit["minute"] == []:
                        t_unit["minute"].append("00")

                if duration_flag == 0:
                    # print(t_unit["year"],t_unit["month"],t_unit["day"],t_unit["minute"],t_unit["hour"])
                    list_text.insert(spans[index][0] + increment,
                                     '<TIME,DATE,' + str(t_unit["year"][0]) + '-' + str(t_unit["month"][0]) + '-' + str(
                                         t_unit["day"][0]) + "T" + str(t_unit["hour"][0]) + ':' + str(
                                         t_unit["minute"][0]) + ':00>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1
                else:
                    list_text.insert(spans[index][0] + increment,
                                     '<TIME,DURATION，' + str(day_src) + 'D' + str(minute_src) + 'm' + '>')
                    increment += 1
                    list_text.insert(spans[index][1] + increment, '</TIME>')
                    increment += 1
                    flag = 1

            if flag != 0:
                continue

        out_text = ''.join(list_text)

        print("It's ok!")

        return out_text

#
#
# t=TimeParse()
#
# t.tipa(text)
