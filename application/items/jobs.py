from application import db
from application.items.models import Item
import datetime
import pytz

def sell_item(item_id):
    item = Item.query.get(item_id)
    item.sell()
    db.session().commit()


def sell_item_job(scheduler, item_id, sell_datetime):
        scheduler.add_job(sell_item, 'date', run_date=sell_datetime, id=item_id, replace_existing=True, kwargs={"item_id":item_id})
