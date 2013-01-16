#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from google.appengine.api import users
from lib.parser import DateTimeParser
from lib.datastore import RemindStatus, TdmessagerHistory

from lib.func import list_reminds
print 'Content-Type: text/plain'
print ''
#text = raw_input("enter the string:")
text = 'test in 1m'

def text_message(text):
    """Handles answers to questions we've asked the user."""
    mail =  'handsomecheung@gmail.com'
    g_user = users.User(mail)

    insert_history = TdmessagerHistory(google_user = g_user, history_string = text)
    insert_history.put()
    parser = DateTimeParser(text)
    if parser.parser_text():
        insert_status = RemindStatus(google_user = g_user, remind_at = parser.target_datetime, subject = parser.remind_content, full_message = text, is_remind = False)
        insert_status.put()
        td_reply = str(parser.local_datetime) + '   ' + parser.remind_content
        print td_reply
    else:
        print parser.err_msg

text_message(text)

g_user = users.User('handsomecheung@gmail.com')
td_reply = list_reminds(g_user)
print td_reply
print '-----------------------------------'
