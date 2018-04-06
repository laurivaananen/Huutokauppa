from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, DateField, validators, ValidationError, TextAreaField

class ItemForm(FlaskForm):
    
    name = StringField("Item name", [validators.Length(min=2)])
    starting_price = IntegerField("Starting price", [validators.NumberRange(min=1)])
    buyout_price = IntegerField("Buyout price", [validators.InputRequired(), validators.NumberRange(min=5)])

    def validate_buyout_price(form, field):
        if type(field.data) is int and type(form.starting_price.data) is int:
            if field.data < form.starting_price.data:
                raise ValidationError("Buyout price has to be bigger then starting price")

    bidding_end = DateField("Bidding end date", [validators.InputRequired()])
    description = TextAreaField("Item description", [validators.Length(min=1, max=4096)])
    quality = StringField("Item quality", [validators.InputRequired()])


    class Meta:
        csrf = False