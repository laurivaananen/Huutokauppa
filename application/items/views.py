from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.items.models import Item
from application.items.forms import ItemForm

@app.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items=Item.query.all())

@app.route("/items/new/")
@login_required
def items_form():
    return render_template("items/new.html", form = ItemForm())

@app.route("/items/<item_id>/", methods=["POST"])
@login_required
def item_sell(item_id):

    item = Item.query.get(item_id)
    item.sold = True
    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    if not form.validate():
        return render_template("items/new.html", form=form)

    item = Item(starting_price = form.starting_price.data,
                buyout_price = form.buyout_price.data,
                name = form.name.data,
                account_id = current_user.id)

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))