from application import celery, db
from application.items.models import Item

@celery.task
def sell_item(item_id):
    try:
        item = Item.query.get(item_id)
        item.sold = True
        item.name = "THIS ITEM HAS BEEN SOLD"
        print("Hello")
        db.session().commit()
        db.session().close()
    except:
        pass

