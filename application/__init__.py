# Flask-sovellus
from flask import Flask, redirect
application = Flask(__name__)
application.config["BCRYPT_LOG_ROUNDS"] = 12

# Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(application)

# Tietokanta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(application)

import os


if os.environ.get("HEROKU"):

    @application.route("/", methods=["POST", "GET"])
    def b_route():
        return redirect("http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/")

    @application.route('/<path:dummy>', methods=["POST", "GET"])
    def redirect_to_aws(dummy):
        return redirect("http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/")

elif os.environ.get("AWS") == "huutokauppa-sovellus":

    user = os.environ.get("PSQL_USER")
    password = os.environ.get("PSQL_PASSWORD")
    host = os.environ.get("PSQL_HOST")
    port = os.environ.get("PSQL_PORT")
    database = os.environ.get("PSQL_DATABASE")

    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, database)

    application.config["SQLALCHEMY_ECHO"] = True

    application.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
    application.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")


    # Celery
    from application.tasks import make_celery


    application.config.update()

    celery = make_celery(application)





    from application import views

    from application.items import models
    from application.items import views

    from application.bid import models, views

    from application.auth import models
    from application.auth import views






else:
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"

    application.config["SQLALCHEMY_ECHO"] = True

    # application.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL")
    # application.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL")

    application.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    application.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"




    # Celery
    from application.tasks import make_celery


    application.config.update()

    celery = make_celery(application)

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
    # return User.query.filter(User.id==userid).first()
    return AccountInformation.query.filter(AccountInformation.id==user_id).first()
    # return AccountInformation.query.get(user_id)

from application.items.models import Quality


try:
    db.create_all()
except:
    pass

@application.before_first_request
def add_qualities():
    if not Quality.query.all():
        new = Quality(name="New")
        used = Quality(name="Used")
        refurbished = Quality(name="Refurbished")

        db.session().add(new)
        db.session().add(used)
        db.session().add(refurbished)
        db.session().commit()