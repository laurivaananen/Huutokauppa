from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.bid.models import Bid
from application.items.models import Item
from application.bid.forms import BidForm



@login_required
@app.route("/bid/create/<item_id>", methods=["POST"])
def bid_create(item_id):
    form = BidForm(request.form)

    if not form.validate():
        item = Item.query.get(item_id)
        return render_template("items/detail.html", item=item, form=form)

    amount = form.amount.data

    bid = Bid(amount=amount, account_information_id=current_user.id, item_id=item_id)

    db.session().add(bid)
    db.session().commit()

    return redirect(url_for("item_detail", item_id=item_id))

