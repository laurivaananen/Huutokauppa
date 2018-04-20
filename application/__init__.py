# Flask-sovellus
from flask import Flask, redirect
application = Flask(__name__)

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
    # application.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    # application.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"








    from application import views

    from application.items import models
    from application.items import views

    from application.bid import models, views

    from application.auth import models
    from application.auth import views






else:
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"



    application.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    application.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"




    # Celery
    from application.tasks import make_celery


    application.config.update()

    celery = make_celery(application)

    @celery.task()
    def printer(text="Here"):
        print(text)


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
