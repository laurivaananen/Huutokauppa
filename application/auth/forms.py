from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    # first_name = StringField("First name", [validators.InputRequired()])
    # last_name = StringField("Last name", [validators.InputRequired()])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False

class SignupForm(FlaskForm):
    first_name = StringField("First name", [validators.InputRequired()])
    last_name = StringField("Last name", [validators.InputRequired()])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False