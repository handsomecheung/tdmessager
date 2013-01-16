#-*- coding: UTF-8 -*-
VERSION = '0.1.0'
date_format_list = ['d', 'h', 'm', 's']

DATE_SEP = ['-', '_', '/', '——']

TIME_SEP = [':', '.', ',', '：', '，', '。']


HELP_INFO = '''
VERSION = %s
在一段时间后提醒："某事 in Xm"，m 为 分钟，也可以使用h（小时）、d（天）。
在具体的时间提醒：“某事 at 月-日-年 hour:minute"，如果使用 12 小时制，在其后加上 am/pm 即可。

显示帮助： help
列出待提醒项： list

示例：
"烧水 in 5m " : 5 分钟后提醒烧水
"收菜 in 1d6h20m" : 1 天 6 小时 20 分钟后提醒收菜
"看《锵锵三人行》 at 20:30" 晚上八点半提醒看《锵锵三人行》
"信用卡还款 at 12-25 9:00 am" 12 月 25 日早上九点提醒信用卡还款
"起床 at 30" 30 分起床

任何问题，email 我： handsomecheung@gmail.com
''' % (VERSION,)
