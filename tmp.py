#-*- coding: UTF-8 -*-

from lib.parser import DateTimeParser
import sys

#s = raw_input('string:')

s = sys.argv[1]

dtp = DateTimeParser(s)
print s
print 'utc_now: %s' % str(dtp.now)
if dtp.parser_text():
#    print dtp.target_datetime
    print dtp.local_datetime
else:
    print dtp.err_msg
