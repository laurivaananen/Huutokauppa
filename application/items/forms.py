from flask_wtf import FlaskForm
# from datetime import datetime, date, time
from flask_wtf.file import FileField, FileRequired
import datetime
from pytz import utc, timezone
import pytz
from wtforms import StringField, IntegerField, BooleanField, DateField, validators, ValidationError, TextAreaField, SelectField, FormField

class DateTimeForm(FlaskForm):
    bidding_end_date = StringField("Bidding end date (yyyy-mm-dd)", [validators.InputRequired(), validators.regexp(r'^\d{4}-\d{2}-\d{2}$', message="You need to give the date in a correct format (yyyy-mm-dd)")])

    bidding_end_time = StringField("Bidding end time (hh:mm)", [validators.InputRequired(), validators.regexp(r'^\d{2}:\d{2}$', message="You need to give the time in a correct format (hh:mm)")])

    def validate_bidding_end_time(form, field):
        if form.bidding_end_date.validate(form) and form.bidding_end_time.validate(form):

            bidding_end = "{} {}".format(form.bidding_end_date.data, form.bidding_end_time.data)
            try:
                bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValidationError("Please enter a correct datetime")

            helsinki = pytz.timezone("Europe/Helsinki")

            bidding_end = helsinki.localize(bidding_end)

            bidding_end = bidding_end.astimezone(utc)

            if datetime.datetime.now().astimezone(utc) > bidding_end:
                raise ValidationError("Please enter a datetime that is in the future")

    class Meta:
        csrf = False


class ItemForm(FlaskForm):
    
    name = StringField("Item name", [validators.InputRequired(), validators.Length(max=144)])
    starting_price = IntegerField("Starting price", [validators.InputRequired(), validators.NumberRange(min=1)])
    bidding_end = FormField(DateTimeForm)
    image = FileField("Image")

    # def validate_image(form, field):
    #     print("\n\n{}\n\n".format(field))
    #     print("\n\n{}\n\n".format(field.data))
    #     print("\n\n{}\n\n".format(field.name))


    @staticmethod
    def get_current_date():
        helsinki = timezone("Europe/Helsinki")
        return datetime.datetime.now(tz=helsinki).strftime("%Y-%m-%d")

    @staticmethod
    def get_current_time():
        helsinki = timezone("Europe/Helsinki")
        return datetime.datetime.now(tz=helsinki).strftime("%H:%M")

    description = TextAreaField("Item description", [validators.InputRequired(), validators.Length(max=4096)])
    quality = SelectField("Quality", coerce=int)

    # class Meta:
    #     csrf = False
