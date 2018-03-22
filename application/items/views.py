from application import app, db
from flask import redirect, render_template, request, url_for
from application.items.models import Item

@app.route("/items", methods=["GET"])
def items_index():
    return render_template("items/list.html", items=Item.query.all())

@app.route("/items/new/")
def items_form():
    return render_template("items/new.html")

@app.route("/items/<item_id>/", methods=["POST"])
def item_sell(item_id):

    item = Item.query.get(item_id)
    item.sold = True
    db.session().commit()

    return redirect(url_for("items_index"))

@app.route("/items/", methods=["POST"])
def items_create():
    item = Item(name=request.form.get("name"),
                starting_price=request.form.get("starting_price"),
                buyout_price=request.form.get("buyout_price"))

    db.session().add(item)
    db.session().commit()

    return redirect(url_for("items_index"))