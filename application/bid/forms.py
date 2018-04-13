from flask_wtf import FlaskForm, Form
from wtforms import StringField, IntegerField, BooleanField, DateField, validators, ValidationError, TextAreaField

class BidForm(FlaskForm):

    amount = IntegerField("Amount", [validators.NumberRange(min=1)])

    def validate(self, latest_bid):
        rv =  Form.validate(self)
        if not rv:
            return False

        if self.amount.data <= latest_bid:
            self.amount.errors.append('You need to bid more than the current bid')
            return False

        return True


    # def validate_amount(form, field):
    #     if type(field.data) is int:
    #         if field.data < form.starting_price.data:
    #             raise ValidationError("Buyout price has to be bigger then starting price")

    class Meta:
        csrf = False