from google.appengine.ext import db

class RemindStatus(db.Model):
    google_user = db.UserProperty(required=True)
    remind_at = db.DateTimeProperty(required = True)
    subject = db.TextProperty(required = True)
    full_message = db.TextProperty(required = True)
    is_remind = db.BooleanProperty(required = True)


class TdmessagerHistory(db.Model):
    google_user = db.UserProperty(required=True)
    history_string = db.TextProperty(required = True)
    add_datetime = db.DateTimeProperty(auto_now = True, auto_now_add = True)
