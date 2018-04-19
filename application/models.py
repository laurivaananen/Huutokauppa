from application import db
import datetime
import pytz

def current_datetime():
    return datetime.datetime.now().astimezone(pytz.utc)

class Base(db.Model):

    __abstract__ = True

    
    
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                              onupdate=datetime.datetime.utcnow)


    def date_created_from_utc(self):
        helsinki = pytz.timezone("Europe/Helsinki")
        utc_date_created = pytz.utc.localize(self.date_created)

        return utc_date_created.astimezone(helsinki).strftime("%Y-%m-%d %H:%M")