from application import celery, db
from application.items.models import Item

@celery.task
def sell_item(item_id):
    item = Item.query.get(item_id)
    item.sold = True
    db.session().commit()
    db.session().close()
