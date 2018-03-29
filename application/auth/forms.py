from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    # first_name = StringField("First name", [validators.InputRequired()])
    # last_name = StringField("Last name", [validators.InputRequired()])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=8, message="Password has to a minimum of 8 characters long.")])

    class Meta:
        csrf = False