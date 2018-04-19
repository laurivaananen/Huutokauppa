# Flask-sovellus
print("first")
from flask import Flask
app = Flask(__name__)

# Tietokanta
from flask_sqlalchemy import SQLAlchemy

import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Scheduler

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import datetime
import pytz


if os.environ.get("HEROKU"):
    jobstores_url = os.environ.get("DATABASE_URL")
else:
    jobstores_url = "sqlite:///application/items.db"

jobstores = {
    'default': SQLAlchemyJobStore(url=jobstores_url)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc)
scheduler.start()


# Oman sovelluksen toiminnallisuudet
from application import views

from application.items import models
from application.items import views

from application.bid import models, views

from application.auth import models
from application.auth import views

# Kirjautuminen
from application.auth.models import UserAccount, AccountInformation
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return AccountInformation.query.get(user_id)

print("stil here")

try:
    db.create_all()
except:
    pass

