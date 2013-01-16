#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from lib.datastore import RemindStatus
from datetime import datetime

def list_reminds(g_user):
    n = datetime.utcnow()
    now_date = datetime.strptime('%s-%s-%s %s:%s' % (n.year, n.month, n.day, n.hour, n.minute), '%Y-%m-%d %H:%M')
    result = RemindStatus.all().filter('is_remind =', False).filter('remind_at >', now_date).filter('google_user =', g_user)
    message = ''
    for r in result:
        message += r.subject + ': ' + str(r.remind_at) + '\n'
    if not message:
        message = u'没有待提醒的消息'
    return message
