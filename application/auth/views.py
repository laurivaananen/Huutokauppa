from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import application, db
from application.extensions import get_or_create
from application.auth.models import UserAccount, AccountInformation, Country, City, PostalCode, StreetAddress
from application.auth.forms import LoginForm, UserSignupForm, AccountDepositForm
from application.items.models import Item

@application.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = AccountInformation.query.filter_by(email_address=form.email_address.data).first()
        if user and user.is_correct_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            form.email_address.errors.append("Wrong password or email address")
            render_template('auth/loginform.html', form=form)
    return render_template('auth/loginform.html', form=form)

@application.route("/auth/logout", methods = ["GET", "POST"])
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@application.route("/auth/user/signup", methods = ["GET", "POST"])
def auth_usersignup():
    if request.method == "GET":
        return render_template("auth/usersignupform.html", form = UserSignupForm())

    form = UserSignupForm(request.form)

    if not form.validate():
        return render_template("auth/usersignupform.html", form=form, error="Error happened")


    country = get_or_create(db.session, Country, name=form.country.data)
    city = get_or_create(db.session, City, name=form.city.data)
    postal_code = get_or_create(db.session, PostalCode, name=form.postal_code.data)
    street_address = get_or_create(db.session, StreetAddress, name=form.street_address.data)

    account_information = AccountInformation(email_address = form.email_address.data,
                                             phone_number = form.phone_number.data,
                                             country = country.id,
                                             city = city.id,
                                             postal_code = postal_code.id,
                                             street_address = street_address.id)

    account_information.set_password(form.password.data)

    db.session.add(account_information)
    db.session.flush()

    user_account = UserAccount(user_name = form.user_name.data,
                               account_information = account_information.id,
                               first_name = form.first_name.data,
                               last_name = form.last_name.data)

    db.session().add(user_account)
    db.session().commit()

    login_user(user_account)
    return redirect(url_for("index"))

@application.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
def user_detail(user_id):
    account_information = AccountInformation.query.get_or_404(user_id)

    items = None
    bought_items = None

    if current_user.is_authenticated() and current_user.id == account_information.id:
        items = account_information.items
        bought_items = account_information.bought_items

    return render_template("auth/detail.html", account_information=account_information, form=AccountDepositForm(), items=items, bought_items=bought_items)
