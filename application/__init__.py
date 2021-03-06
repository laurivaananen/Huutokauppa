# Flask-sovellus
from flask import Flask, redirect
import os
application = Flask(__name__)
application.config["BCRYPT_LOG_ROUNDS"] = 12
application.config["UPLOAD_FOLDER"] = os.getcwd() + "/application/static/images"
application.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
# application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:huutokauppapassword@huutokauppa_postgres:5432/postgres"


application.config["SQLALCHEMY_ECHO"] = True

application.config["CELERY_BROKER_URL"] = "redis://huutokauppa_redis:6379/0"
application.config["CELERY_RESULT_BACKEND"] = "redis://huutokauppa_redis:6379/0"
# Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(application)

# Tietokanta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(application)


from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import url_for
from application.models import Base
from application.extensions import get_or_create
from application.auth.models import Country, City, PostalCode, StreetAddress, AccountInformation, UserAccount
from application.items.models import Item, Quality, Category
from application.bid.models import Bid

from application.auth import models
from application.items import models
from application.bid import models
from application import models

print("\n\nCreating db\n\n")
db.create_all()
print("\n\ncreated db\n\n")

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'password',
#     'db': 'my_database',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


from application.tasks import make_celery


application.config.update()

celery = make_celery(application)

from application import views

from application.items import models
from application.items import views

from application.bid import models, views

from application.auth import models
from application.auth import views


@application.route("/", methods=["POST", "GET"])
def b_route():
    return redirect(url_for('index'))

@application.route('/<path:dummy>', methods=["POST", "GET"])
def redirect_to_aws(dummy):
    return redirect(url_for('index'))

# Kirjautuminen
from application.auth.models import UserAccount, AccountInformation
from os import urandom
application.config["SECRET_KEY"] = urandom(32)



from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(application)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

@login_manager.user_loader
def load_user(user_id):
    return AccountInformation.query.filter(AccountInformation.id==user_id).first()


# Admin



# Inheriting from the default admin view and adding authentication checks
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            account_information = AccountInformation.query.get_or_404(current_user.id)
            return account_information.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class SecureModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            account_information = AccountInformation.query.get_or_404(current_user.id)
            return account_information.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class ItemModelView(SecureModelView):
    form_ajax_refs = {
        'bids': {
            'fields': (Bid.amount, )
        }
    }


class AccountInformationModelView(SecureModelView):
    form_ajax_refs = {
        'items': {
            'fields': (Item.name, )
        }
    }

admin = Admin(application, name="Huutokauppa", template_mode="bootstrap3", index_view=SecureAdminIndexView())
admin.add_view(AccountInformationModelView(AccountInformation, db.session))
admin.add_view(ItemModelView(Item, db.session))
admin.add_view(SecureModelView(Bid, db.session))
admin.add_view(SecureModelView(Quality, db.session))
admin.add_view(SecureModelView(Category, db.session))
admin.add_view(SecureModelView(UserAccount, db.session))






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

@application.before_first_request
def add_categories():
    if not Category.query.all():
        electronics = Category(name="Electronics")
        home = Category(name="Home")
        books = Category(name="Books")
        sports = Category(name="Sports")
        art = Category(name="Art")

        db.session().add(electronics)
        db.session().add(home)
        db.session().add(books)
        db.session().add(sports)
        db.session().add(art)
        db.session().commit()

# Adding an admin account when application is run for the first time
@application.before_first_request
def add_super_admin():
    if not AccountInformation.query.all():
        country = get_or_create(db.session, Country, name="admin")
        city = get_or_create(db.session, City, name="admin")
        postal_code = get_or_create(db.session, PostalCode, name="admin")
        street_address = get_or_create(db.session, StreetAddress, name="admin")

        account_information = AccountInformation(email_address = "admin@email.com",
                                             phone_number = "admin",
                                             country = country.id,
                                             city = city.id,
                                             postal_code = postal_code.id,
                                             street_address = street_address.id)

        account_information.set_password("based_god")
        account_information.is_admin = True

        db.session.add(account_information)
        db.session.flush()

        user_account = UserAccount(user_name = "admin",
                                account_information = account_information.id,
                                first_name = "admin",
                                last_name = "admin")

        db.session().add(user_account)
        db.session().commit()
