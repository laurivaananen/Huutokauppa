from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import UserAccount, AccountInformation
from application.auth.forms import LoginForm, UserSignupForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form=form)

    user = AccountInformation.query.filter_by(email_address=form.email_address.data,
                                password=form.password.data).first()

    if not user:
        return render_template("auth/loginform.html", form=form, error="No such email address or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout", methods = ["GET", "POST"])
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/user/signup", methods = ["GET", "POST"])
def auth_usersignup():
    if request.method == "GET":
        return render_template("auth/usersignupform.html", form = UserSignupForm())

    form = UserSignupForm(request.form)

    if not form.validate():
        return render_template("auth/usersignupform.html", form=form, error="Error happened")

    account_information = AccountInformation(email_address = form.email_address.data,
                                             password = form.password.data,
                                             phone_number = form.phone_number.data,
                                             country = form.country.data,
                                             city = form.city.data,
                                             postal_code = form.postal_code.data,
                                             street_address = form.street_address.data)

    db.session.add(account_information)
    db.session().commit()


    user_account = UserAccount(user_name = form.user_name.data,
                               account_informations = AccountInformation.query.filter_by(email_address = account_information.email_address).first().id,
                               first_name = form.first_name.data,
                               last_name = form.last_name.data)

    db.session().add(user_account)
    db.session().commit()

    

    login_user(user_account)
    return redirect(url_for("index"))
