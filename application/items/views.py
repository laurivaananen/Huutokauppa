from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.items.models import Item, Quality, Image
from application.items.forms import ItemForm
from application.extensions import get_or_create
from application.bid.forms import BidForm

@app.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items=Item.query.all())

@app.route("/items/new/")
@login_required
def items_form():
    return render_template("items/new.html", form = ItemForm())

@app.route("/items/<item_id>/", methods=["GET"])
def item_detail(item_id):

    item = Item.query.get(item_id)

    return render_template("items/detail.html", item=item, form=BidForm())

@login_required
@app.route("/items/edit/<item_id>/", methods=["GET"])
def item_edit(item_id):

    item = Item.query.get(item_id)

    return render_template("items/edit.html", item=item, form=ItemForm(obj=item))

@login_required
@app.route("/items/update/<item_id>/", methods=["POST"])
def item_update(item_id):

    item = Item.query.get(item_id)
    if current_user.id == item.AccountInformation.id:
        form = ItemForm(request.form)
        item.name = form.name.data

        if form.buyout_price.data >= item.buyout_price:
            item.buyout_price = form.buyout_price.data

        item.description = form.description.data

        if form.bidding_end.data >= item.bidding_end:
            item.bidding_end = form.bidding_end.data

        if item.Quality.name != form.quality.data:
            quality = get_or_create(db.session, Quality, name=form.quality.data)
            item.quality = quality.id

        db.session().commit()

    return redirect(url_for("item_detail", item_id=item.id))

@app.route("/items/delete/<item_id>/", methods=["POST"])
@login_required
def item_delete(item_id):

    item = Item.query.get(item_id)
    if current_user.id == item.AccountInformation.id:
        db.session().delete(item)
        db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form=form)

    quality = get_or_create(db.session, Quality, name=form.quality.data)

    item = Item(starting_price = form.starting_price.data,
                buyout_price = form.buyout_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = quality.id,
                description = form.description.data,
                bidding_end = form.bidding_end.data)

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))