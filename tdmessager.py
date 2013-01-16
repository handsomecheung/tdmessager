#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
#from google.appengine.ext import db
from google.appengine.api import xmpp
from datetime import datetime

from lib.datastore import RemindStatus

print 'Content-Type: text/plain'
print ''
print 'testing page'

n = datetime.utcnow()
now_date = datetime.strptime('%s-%s-%s %s:%s' % (n.year, n.month, n.day, n.hour, n.minute), '%Y-%m-%d %H:%M')
limit = 10

while True:
    result = RemindStatus.all().filter('is_remind =', False).filter('remind_at =', now_date)
    print result.count()

    reminds = result.fetch(limit)

    for r  in reminds:
        print '1 remind'
        status_code = xmpp.send_message(r.google_user.email(), r.subject)
        r.is_remind = True
        r.put()
        if status_code != xmpp.NO_ERROR:
            pass
        else:
            print 'remind sent'

    if limit > result.count:
        result = RemindStatus.all().filter('is_remind =', False).filter('remind_at =', now_date)
    else:
        break
