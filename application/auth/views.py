from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, SignupForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form=form)

    user = User.query.filter_by(email_address=form.email_address.data,
                                password=form.password.data).first()

    if not user:
        return render_template("auth/loginform.html", form=form, error="No such email address or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout", methods = ["GET", "POST"])
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/signup", methods = ["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signupform.html", form = SignupForm())

    form = SignupForm(request.form)
    print(form.first_name.data)
    print(form.last_name.data)
    print(form.email_address.data)
    print(form.password.data)

    if not form.validate():
        return render_template("auth/signupform.html", form=form, error="Error happened")

    user = User(first_name = form.first_name.data,
                last_name = form.last_name.data,
                email_address = form.email_address.data,
                password = form.password.data)

    db.session().add(user)
    db.session().commit()

    login_user(user)
    return redirect(url_for("index"))
