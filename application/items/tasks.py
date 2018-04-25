from application import celery, db
from application.items.models import Item
from application.bid.models import Bid
from application.auth.models import AccountInformation

@celery.task
def sell_item(item_id):
    print("\n\n\n\nStarting task\n\n\n\n")
    item = Item.query.get(item_id)
    item.sold = True

    highest_bid = item.highest_bid(item_id)
    print(highest_bid)
    if highest_bid:
        bid = Bid.query.get(highest_bid)
        bid_account = AccountInformation.query.get(bid.account_information_id)
        print(bid_account)
        print(item.buyer_account_information_id)
        item.buyer_account_information_id = bid_account.id

    db.session().commit()
    db.session().close()
