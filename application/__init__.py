# Flask-sovellus
from flask import Flask
app = Flask(__name__)

# Tietokanta
from flask_sqlalchemy import SQLAlchemy

import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

db = SQLAlchemy(app)

# Celery
from application.tasks import make_celery


app.config.update()

celery = make_celery(app)

@celery.task()
def printer(text="Here"):
    print(text)


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

try:
    db.create_all()
except:
    pass
