import re
import datetime

UTIL_CN_NUM = {
    '〇':0,'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,'廿':20,'卅':30,'卌':40,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    r'\uFF10':0,r'\uFF11':1,r'\uFF12':2,r'\uFF13':3,r'\uFF14':4,r'\uFF15':5,r'\uFF16':6,r'\uFF17':7,r'\uFF18':8,r'\uFF19':9
}

UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}

# def sim2dig(src):
#     digstr=""
#     rsl = 0
#     unit = 1
#     for item in src[::-1]:
#         if item in UTIL_CN_UNIT.keys():
#             unit = UTIL_CN_UNIT[item]
#         elif item in UTIL_CN_NUM.keys():
#             num = UTIL_CN_NUM[item]
#             rsl += num * unit
#     if rsl < unit:
#         rsl += unit
#     return rsl

def cn2dig(src):
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return rsl

def year2dig(year):
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    m = re.match("\d+", res)
    if m:
        if len(m.group(0)) == 2:
            return int(datetime.datetime.today().year / 100) * 100 + int(m.group(0))
        else:
            return int(m.group(0))
    else:
        return None
