from flask import render_template
from application import application
from application.auth.models import AccountInformation
from application.items.models import Item

@application.route("/")
def index():
    top_sellers = AccountInformation.top_sellers()
    top_bidders = AccountInformation.top_bidders()
    hot_items = Item.hot_items()
    print("\n\n")
    print(hot_items)
    trending_items = []
    for xx in hot_items:
        print(xx)
        xx["bidding_time_left"] = Item.bidding_time_left(xx["id"])
        xx["end_date"] = Item.utc_quick(item_id=xx["id"])
        trending_items.append(xx)
    print("\n\n")
    print(trending_items)
    return render_template("index.html", top_sellers=top_sellers, top_bidders=top_bidders, hot_items=trending_items)


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404