from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.items.models import Item, Quality, Image
from application.items.forms import ItemForm
from application.extensions import get_or_create

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

    return render_template("items/detail.html", item=item)

# @app.route("/items/<item_id>/", methods=["POST"])
# @login_required
# def item_sell(item_id):

#     item = Item.query.get(item_id)
#     item.sold = True
#     db.session().commit()

#     return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form=form)

    quality_id = get_or_create(db.session, Quality, name=form.quality.data)

    item = Item(starting_price = form.starting_price.data,
                buyout_price = form.buyout_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality_id = quality_id.id,
                description = form.description.data,
                bidding_end = form.bidding_end.data)

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))