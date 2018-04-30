from application import application, db
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from application.items.models import Item, Quality
from application.items.forms import ItemForm
from application.items.tasks import sell_item
from application.extensions import get_or_create
from application.bid.forms import BidForm
from application.bid.models import Bid
import datetime
from pytz import utc
import pytz
from werkzeug.utils import secure_filename
import os

@application.route("/items/", methods=["GET"])
def items_index():
    # items = Item.query.filter_by(sold=False, hidden=False).order_by(Item.bidding_end.asc()).paginate(1, 1, error_out=False)
    # next_page = None
    # if items.has_next:
    #     next_page = items.next_num
    return render_template("items/list.html", items=None, next_page=None)

@application.route("/loaditems")
def load_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.filter_by(sold=False, hidden=False).order_by(Item.bidding_end.asc()).paginate(page, 5, error_out=False)

    next_page = None
    if items.has_next:
        next_page = items.next_num

    return jsonify(items=[{"name": item.name,
                           "starting_price": item.starting_price,
                           "id": item.id,
                           "latest_bid": item.latest_bid(),
                           "bidding_time_left": item.bidding_time_left(),
                           "bidding_end": item.datetime_from_utc(),
                           "quality": item.quality.name,
                           "seller": item.account_information.user_account.user_name,
                           "seller_id": item.account_information_id} for item in items.items],
                           next_page=next_page)


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
    bids = Bid.query.filter_by(item_id=item_id).order_by(Bid.amount.desc()).limit(7)

    return render_template("items/detail.html", item=item, form=BidForm(), bids=bids)

@login_required
@application.route("/items/edit/<item_id>/", methods=["GET"])
def item_edit(item_id):

    item = Item.query.get(item_id)

    form = ItemForm(obj=item)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not item.sold and not item.hidden:
        if current_user.id is item.account_information_id:
            return render_template("items/edit.html", item=item, form=form)
        else:
            return redirect(url_for('items_index'))

    else:
        return redirect(url_for('items_index'))

@login_required
@application.route("/items/update/<item_id>/", methods=["POST"])
def item_update(item_id):

    form = ItemForm(request.form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not (form.name.validate(form) and (form.description.validate(form)) and (form.quality.validate(form))):
        return render_template("items/edit.html", form=form, item=Item.query.get(item_id))

    item = Item.query.get_or_404(item_id)
    if not item.sold and not item.hidden:
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
    if not item.sold and not item.hidden:
        if current_user.id == item.account_information.id:
            db.session().delete(item)
            db.session().commit()

    return redirect(url_for("items_index"))

@application.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not form.validate():
        return render_template("items/new.html", form=form)

    helsinki = pytz.timezone("Europe/Helsinki")

    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)

    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")

    bidding_end = helsinki.localize(bidding_end)

    bidding_end = bidding_end.astimezone(utc)

    # print("\n\n{}\n\n".format(form.image))
    # print("\n\n{}\n\n".format(form.image.name))
    # print("\n\n{}\n\n".format(request.files))
    # print("\n\n{}\n\n".format(request.files.get("image")))
    # print("\n\n{}\n\n".format(request.files.get("image").filename))
    # print("\n\n{}\n\n".format(os.getcwd()))
    # print("\n\n{}\n\n".format(application.config["UPLOAD_FOLDER"]))

    image_file = request.files.get("image")

    sec_filename = secure_filename(image_file.filename)

    timecode = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    image_file.save(os.path.join(application.config["UPLOAD_FOLDER"], "{}-{}".format(sec_filename, timecode)))

    item = Item(starting_price = form.starting_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = form.quality.data,
                description = form.description.data,
                bidding_end = bidding_end)

    db.session().add(item)
    db.session().commit()

    sell_item.apply_async(args=[item.id], eta=bidding_end)

    return redirect(url_for("items_index"))
