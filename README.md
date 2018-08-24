# Pan-Timer

#### 项目介绍

中文时间表达式识别、归类、归一化

#### 说明

1. 时间表达式识别与归一化项目的python3版本
2. 分类标准TIMEX3（DATE点时间、SET重复时间、FUZZY模糊时间、DURATION段时间）
3. 归一化标准ISO8061（Y 年、M 月、W 周、D 日、h 时、m 分、s 秒）
4. 依赖库 DateTime 4.2


#### 参与贡献
- 作者：Lucky-Dong

#### 使用说明
- 请打开main.py文件 将需要识别的文件或字符串以字符串形式传入tipa()函数
- TimeRecognition.py为识别模块
- TimeReg.py为识别正则化文件
- TimeParse.py为归一化模块
- test.txt为测试文件
- outcome.txt为测试输出文件

#### 样例
```
text='''
        10：20-16：30
        每3个月休一次假期
        2019年3月7日至2019年4月1日
        1993年植树节
        小明在7月六号早上8点买了瓶1982年9月生产的雷碧
        上课时间为7-9月份
        2020年元旦快乐！！

    '''
```

```
    <TIME,DURATION,370m>10：20-16：30</TIME>
    <TIME,SET,E3M>每3个月</TIME>休一次假期
    <TIME,DURATION，25D0m>2019年3月7日至2019年4月1日</TIME>
    <TIME,DATE,1993-03-12T00:00:00>1993年植树节</TIME>
    小明在<TIME,DATE,0000-7-6T8:00:00>7月六号早上8点</TIME>买了瓶<TIME,DATE,1982-9-00T00:00:00>1982年9月</TIME>生产的雷碧
    上课时间为<TIME,DURATION,2M>7-9月份</TIME>
    <TIME,DATE,2020-01-01T00:00:00>2020年元旦</TIME>快乐！！

```
