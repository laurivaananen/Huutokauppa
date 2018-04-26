from application import celery, db
from application.items.models import Item
from application.bid.models import Bid
from application.auth.models import AccountInformation

@celery.task
def sell_item(item_id):
    print("\n\n\n\nStarting task\n\n\n\n")
    item = Item.query.get(item_id)

    highest_bid = item.highest_bid(item_id)
    if highest_bid:
        item.sold = True
        bid = Bid.query.get(highest_bid)
        item.buyer_account_information_id = bid.account_information_id
    else:
        item.hidden = True

    db.session().commit()
    db.session().close()
