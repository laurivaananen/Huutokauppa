from application import celery, db, application
import os
from application.items.models import Item
from application.bid.models import Bid
from application.auth.models import AccountInformation
from celery.states import REVOKED
from application.extensions import put_object_to_s3, generate_presigned_url
from io import BytesIO
from PIL import Image

@celery.task
def sell_item(item_id):
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

def delete_task(idd):
    celery.control.revoke(idd, terminate=True)

@celery.task
def image_to_s3(file_key, item_id):
    # bytes_stream = BytesIO()
    # image_bytes.save(bytes_stream, "PNG")

    with open(os.path.join(application.config["UPLOAD_FOLDER"], file_key), "rb") as f:
        img = f.read()

    put_object_to_s3(image_bytes=img, filename=file_key)
    s3_image_url = generate_presigned_url(filename=file_key)
    
    item = Item.query.get(item_id)
    item.image = s3_image_url

    db.session().commit()
    db.session().close()