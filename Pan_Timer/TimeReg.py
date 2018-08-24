import re
import os


class TimeReg:

    time_rex=[r'([一二]{0,1}[零〇一二三四五六七八九十同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][上中下]午|',
              r'[自从]?([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+[年月日号天时点分][份]?)+[起]?至([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+[年月日号天时点分][份]?)+[止]?|',
              r'([0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+年)?(植树节|圣诞节|青年节|教师节|儿童节|元旦|国庆|劳动节|妇女节|建军节|航海日节|建党节|记者节)|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号]([凌早]晨|[傍夜]晚|[早晚]上|[上中下]午)?[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}[时点:：]?[整许左前]?[右后]?[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}[分]?[许左前]?[右后]?|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][凌早]晨|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][傍夜]晚|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][早晚]上|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][早晚]|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号][左前][右后]|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年\w{1,2}月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,3}[日号]|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}月([上中下]旬)?|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}月[末底初]|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+年[初终底末中春夏秋冬]*|',
              r'[一二]{0,1}[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19同去后明前]+月[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{1,2}[日号]([凌早]晨|[傍夜]晚|[早晚]上|[上中下]午)?[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}[时点:：]?[整许左前]?[右后]?[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,2}[分]?[许左前]?[右后]?|',
              r'[零〇一二三四五六七八九十]{1,3}个[年月日天]|',
              r'(?<=[\[（])\d+(?=[\]）])|',
              r'[零〇一二三四五六七八九十]、[零〇一二三四五六七八九十][年月日]|',
              r'[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+[日月年天]内|',  #段时间
              r'[每/][0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]{0,3}[个]?(年|月|日|天|小时|时|分钟|分|秒)|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[上中下]午\d{1,2}时[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[上中下]午\d{1,2}点|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[凌早]晨\d{1,2}时[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[傍夜]晚\d{1,2}时[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[早晚]上\d{1,2}时[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[早晚]\d{1,2}时[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}时[左前][右后]|',
              '\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}|',
              r'\d{1,2}[:：]\d{1,2}-\d{1,2}[:：]\d{1,2}|',  # 段时间
              '\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}：\d{1,2}|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[上中下]午|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[凌早]晨|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[傍夜]晚|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[早晚]上|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[早晚]|',
              '\d{2,4}年\d{1,2}月\d{1,2}日[左前][右后]|',
              '\d{2,4}年\d{0,2}[月]*\d{0,2}[日]*[夜]*[当]*[天]*\d{0,2}[时]*[许]*\d{0,2}[分]*[左]*[右]*[许]*秒|',
              '\d{2,4}年\d{0,2}[月]*\d{0,2}[日]*[夜]*[当]*[天]*\d{0,2}[时]*[许]*\d{0,2}[分]*[左]*[右]*[许]*|',
              '\d{2,4}年\d{1,2}月\d{1,2}日\d{1,2}时|',
              '\d{2,4}年\d{1,2}月\d{1,2}日|',
              r'(?:[0-9〇零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+\w)?([0-9零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)-([0-9零一二两三四五六七八九十廿卅卌\uFF10-\uFF19]+)(?!:)[年月日周号小时分点秒]|',
              '\d{2,4}年\d{1,2}月[末底初]|',
              '\d{2,4}年\d{1,2}月[上中下]旬|',
              '\d{2,4}年\d{1,2}月|',
              '[零〇一二三四五六七八九十同去后明前]+年\d{1,2}月\d{1,2}[日号]|',
              '\d{1,2}月\d{1,2}日\d{1,2}：\d{1,2}|',
              '\d{1,2}月\d{1,2}日\d{1,2}:\d{1,2}|',
              '\d{1,4}、\d{1,4}[年月日号]',
              '\d{1,4}[年月日]|',
              '\d{1,4}[多]*分钟(左右|许)?|',
              '[上下中]午\d{1,2}点|',
              r'[上下中]午\d{1,2}时\d{1,2}分|',
              '[上下中]午\d{1,2}时|',
              r'([上下中]午|晚[上]?|早[上]?|凌晨)?(\d{1,2})[:：](\d{1,2})[分]?|',
              '\d{1,2}\.\d{1,2}小时|',
              '[半一二三四五六七八九十1-9]+[个]?[多]?小时|',
              '\d{1,3}小时\d{1,3}分|',
              '\d{1,3}小时-\d{1,3}小时|',
              '\d{1,3}小时|',
              '\d{1,2}时\d{1,2}分[左前][右后]|',
              '\d{1,2}时\d{1,2}分|',
              '\d{1,4}[余]?年|',
              r'\d{1,2}个月|',
              r'\d{1,2}月|',
              r'\d{1,3}-\d{1,3}[个]?月份|',
              r'\d{1,3}-\d{1,3}[个]?[日天月]|',
              r'\d{1,3}-\d{1,3}[个]?时|',
              '\d{1,3}日|',
              '\d{1,2}周|',
              '\d{1,2}时|',
              '\d{1,3}\.\d{1,2}天|',
              '\d{1,3}多天|',
              '\d{1,3}[天月日年周]|',
              '\d{1,3}[个]?小时|',
              '([上下中]午|晚[上]?|早[上]?|凌晨)?\d{1,2}点|',
              '\d{4}-\d{1,2}-\d{1,2}|',
              '\d{1,2}:\d{1,2}:\d{1,2}|',
              '\d{1,2}：\d{1,2}：\d{1,2}|',
              r'\d{1,2}月份|',
              '[上下中]午|',
              '星期[一二三四五六天日]|',
              '[春夏秋冬][天季]|',
              '[当目]前|',
              '现[在今]|',
              '(最近|那时|刚刚)|',
              '[明今][天]?[早晚夜]|',
              '天天|',
              '\d{4}\.\d{1,2}\.\d{1,2})',
              ]

    date_pattern = ''.join(time_rex)
    time_reg=re.compile(date_pattern)





