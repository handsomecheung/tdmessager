#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from google.appengine.ext import webapp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from lib.parser import DateTimeParser
from lib.datastore import RemindStatus, TdmessagerHistory
from lib.const import HELP_INFO
from lib.func import list_reminds

HINT_INFO = u'\n使用示例：\n 看表演 at 7:30 pm \n 写日记 in 1h30m \n help 查看帮助'

class XmppHandler(xmpp_handlers.CommandHandler):
    """Handler class for all XMPP activity."""

    def text_message(self, message = None):
        """Handles answers to questions we've asked the user."""
        mail = message.sender[0:message.sender.find('/')]
        g_user = users.User(mail)
        text = message.body

        insert_history = TdmessagerHistory(google_user = g_user, history_string = text)
        insert_history.put()

        t = text.lower()
        if t == 'help':
            return self.help_command(message)
        elif t == 'list':
            return self.list_command(message)

        parser = DateTimeParser(text)
        if parser.parser_text():
            insert_status = RemindStatus(google_user = g_user, remind_at = parser.target_datetime, subject = parser.remind_content, full_message = text, is_remind = False)
            insert_status.put()
            td_reply = '将在' + str(parser.local_datetime) + '提醒你' + parser.remind_content
            message.reply(td_reply)
        else:
            message.reply(parser.err_msg + HINT_INFO)

    def help_command(self, message = None):
        message.reply(HELP_INFO)

    def list_command(self, message = None):
        mail = message.sender[0:message.sender.find('/')]
        g_user = users.User(mail)
        td_reply = list_reminds(g_user)

        message.reply(td_reply)

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XmppHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
