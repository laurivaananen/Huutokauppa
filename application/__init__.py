# Flask-sovellus
from flask import Flask
application = Flask(__name__)

# Tietokanta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(application)

import os
if os.environ.get("HEROKU"):
    application.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    application.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
    application.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")
else:
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
<<<<<<< 718b4574c1622dc7686ba99ae557849182e23b00
    application.config["SQLALCHEMY_ECHO"] = True
    application.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    application.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
=======


    from application import views

    from application.items import models
    from application.items import views

    from application.bid import models, views

    from application.auth import models
    from application.auth import views



<<<<<<< cd1fe4cd014bdbf142128e0266910dfe0b2fd341




>>>>>>> Added db earlier to init

db = SQLAlchemy(application)
=======
>>>>>>> Added db earlier to init

# Celery
from application.tasks import make_celery


application.config.update()

celery = make_celery(application)

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
application.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(application)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return AccountInformation.query.get(user_id)

try:
    db.create_all()
except:
    pass
