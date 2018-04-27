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

@application.route("/items/", methods=["GET"])
def items_index():
    items = Item.query.filter_by(sold=False, hidden=False).order_by(Item.bidding_end.asc()).all()
    print("\n\n\n{}\n\n\n".format(items))
    return render_template("items/list.html", items=items)

@application.route("/items/new/")
@login_required
def items_form():
    form = ItemForm()
    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]
    return render_template("items/new.html", form = form)

@application.route("/items/<item_id>/", methods=["GET"])
def item_detail(item_id):

    item = Item.query.get_or_404(item_id)
    bids = Bid.query.filter_by(item_id=item_id).order_by(Bid.amount.desc())

    return render_template("items/detail.html", item=item, form=BidForm(), bids=bids)

@login_required
@application.route("/items/edit/<item_id>/", methods=["GET"])
def item_edit(item_id):

    item = Item.query.get(item_id)

    form = ItemForm(obj=item)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    return render_template("items/edit.html", item=item, form=form)

@login_required
@application.route("/items/update/<item_id>/", methods=["POST"])
def item_update(item_id):

    form = ItemForm(request.form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not (form.name.validate(form) and (form.description.validate(form)) and (form.quality.validate(form))):
        return render_template("items/edit.html", form=form, item=Item.query.get(item_id))

    item = Item.query.get_or_404(item_id)
    if current_user.id == item.account_information.id:
        
        item.name = form.name.data

        item.description = form.description.data

        item.quality_id = form.quality.data

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

    print(form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not form.validate():
        return render_template("items/new.html", form=form)

    # quality = get_or_create(db.session, Quality, name=form.quality.data)

    helsinki = pytz.timezone("Europe/Helsinki")

    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)

    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")

    bidding_end = helsinki.localize(bidding_end)

    bidding_end = bidding_end.astimezone(utc)

    item = Item(starting_price = form.starting_price.data,
                buyout_price = form.buyout_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = form.quality.data,
                description = form.description.data,
                bidding_end = bidding_end)

    db.session().add(item)
    db.session().commit()

    sell_item.apply_async(args=[item.id], eta=bidding_end)

    return redirect(url_for("items_index"))