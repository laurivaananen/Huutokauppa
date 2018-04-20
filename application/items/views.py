from application import application, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.items.models import Item, Quality, Image
from application.items.forms import ItemForm
from application.items.tasks import sell_item
from application.extensions import get_or_create
from application.bid.forms import BidForm
from application.bid.models import Bid
import datetime
from pytz import utc
import pytz

@application.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items=Item.query.all())

@application.route("/items/new/")
@login_required
def items_form():
    return render_template("items/new.html", form = ItemForm())

@application.route("/items/<item_id>/", methods=["GET"])
def item_detail(item_id):

    item = Item.query.get(item_id)
    bids = Bid.query.filter_by(item_id=item_id)

    sell_item.delay(item_id)

    return render_template("items/detail.html", item=item, form=BidForm(), bids=bids)

@login_required
@application.route("/items/edit/<item_id>/", methods=["GET"])
def item_edit(item_id):

    item = Item.query.get(item_id)

    form = ItemForm(obj=item)

    return render_template("items/edit.html", item=item, form=form)

@login_required
@application.route("/items/update/<item_id>/", methods=["POST"])
def item_update(item_id):

    form = ItemForm(request.form)

    if not (form.name.validate(form) and form.description.validate(form) and form.quality.validate(form)):
        return render_template("items/edit.html", form=form)

    item = Item.query.get(item_id)
    if current_user.id == item.account_information.id:
        
        item.name = form.name.data

        item.description = form.description.data

        if item.quality.name != form.quality.data:
            quality = get_or_create(db.session, Quality, name=form.quality.data)
            item.quality_id = quality.id

        db.session().commit()

    return redirect(url_for("item_detail", item_id=item.id))

@application.route("/items/delete/<item_id>/", methods=["POST"])
@login_required
def item_delete(item_id):

    item = Item.query.get(item_id)
    if current_user.id == item.account_information.id:
        db.session().delete(item)
        db.session().commit()

    return redirect(url_for("items_index"))

@application.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form=form)

    quality = get_or_create(db.session, Quality, name=form.quality.data)

    helsinki = pytz.timezone("Europe/Helsinki")

    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)

    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")

    bidding_end = helsinki.localize(bidding_end)

    bidding_end = bidding_end.astimezone(utc)

    item = Item(starting_price = form.starting_price.data,
                buyout_price = form.buyout_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = quality.id,
                description = form.description.data,
                bidding_end = bidding_end)

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))