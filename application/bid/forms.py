from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, DateField, validators, ValidationError, TextAreaField

class BidForm(FlaskForm):

    amount = IntegerField("Amount", [validators.NumberRange(min=1)])

    class Meta:
        csrf = False