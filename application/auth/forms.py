from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, IntegerField, ValidationError
from application.auth.models import AccountInformation

class LoginForm(FlaskForm):
    # first_name = StringField("First name", [validators.InputRequired()])
    # last_name = StringField("Last name", [validators.InputRequired()])
    email_address = StringField("Email address")
    password = PasswordField("Password")

    def validate_email_address(form, field):
        user = AccountInformation.query.filter_by(email_address=form.email_address.data,
                                password=form.password.data).first()

        if not user:
            raise ValidationError("Wrong password or email address")

    class Meta:
        csrf = False

class UserSignupForm(FlaskForm):
    first_name = StringField("First name", [validators.InputRequired(), validators.Length(max=144)])
    last_name = StringField("Last name", [validators.InputRequired(), validators.Length(max=144)])
    user_name = StringField("User name", [validators.InputRequired(), validators.Length(max=144)])
    email_address = StringField("Email address", [validators.InputRequired(), validators.Email(), validators.Length(max=144)])
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(max=144), validators.EqualTo("repeat_password", message="Passwords must match")])
    repeat_password = PasswordField("Repeat password", [validators.InputRequired()])
    phone_number = StringField("Phone number", [validators.InputRequired(), validators.Length(max=144)])
    country = StringField("Country", [validators.InputRequired(), validators.Length(max=144)])
    city = StringField("City", [validators.InputRequired(), validators.Length(max=144)])
    postal_code = StringField("Postal code", [validators.InputRequired(), validators.Length(max=144)])
    street_address = StringField("Street address", [validators.InputRequired(), validators.Length(max=144)])

    class Meta:
        csrf = False

class AccountDepositForm(FlaskForm):
    amount = IntegerField("Amount", [validators.NumberRange(min=1)])

    class Meta:
        csrf = False