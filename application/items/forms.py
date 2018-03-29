from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators, ValidationError

class ItemForm(FlaskForm):
    starting_price = IntegerField("Starting price", [validators.NumberRange(min=1)])
    buyout_price = IntegerField("Buyout price", [validators.InputRequired()])

    def validate_buyout_price(form, field):
        try:
            if field.data < form.starting_price.data:
                raise ValidationError("Buyout price has to be bigger then starting price")
        except:
            raise ValidationError("Error validating input")
    name = StringField("Item name", [validators.Length(min=2)])

    class Meta:
        csrf = False