from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    # first_name = StringField("First name", [validators.InputRequired()])
    # last_name = StringField("Last name", [validators.InputRequired()])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False

class UserSignupForm(FlaskForm):
    first_name = StringField("First name", [validators.InputRequired()])
    last_name = StringField("Last name", [validators.InputRequired()])
    user_name = StringField("User name", [validators.InputRequired()])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])
    phone_number = StringField("Phone number", [validators.InputRequired()])
    country = StringField("Country", [validators.InputRequired()])
    city = StringField("City", [validators.InputRequired()])
    postal_code = StringField("Postal code", [validators.InputRequired()])
    street_address = StringField("Street address", [validators.InputRequired()])

    class Meta:
        csrf = False