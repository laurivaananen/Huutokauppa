from application import celery, db, application
import os
from application.items.models import Item
from application.bid.models import Bid
from application.auth.models import AccountInformation
from celery.states import REVOKED
from io import BytesIO
from PIL import Image
from application.extensions import put_object_to_s3, generate_presigned_url

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
    # Read image from storage
    with open(os.path.join(application.config["UPLOAD_FOLDER"], "{}.png".format(file_key)), "rb") as f:
        img = Image.open(BytesIO(f.read()))

    thumbnail_image = create_thumbnail(img)
    full_image = create_full(img)

    thumbnail_image = thumbnail_image.convert('RGB')
    thumbnail_image_bytes_stream = BytesIO()
    thumbnail_image.save(thumbnail_image_bytes_stream, "JPEG", quality=70)

    full_image = full_image.convert('RGB')
    full_image_bytes_stream = BytesIO()
    full_image.save(full_image_bytes_stream, "JPEG", quality=75)

    # Save thumbnail image to s3 and get the url
    thumbnail_image_key = "{}-400".format(file_key)
    put_object_to_s3(image_bytes=thumbnail_image_bytes_stream.getvalue(), filename=thumbnail_image_key)
    thumbnail_image_url = generate_presigned_url(filename=thumbnail_image_key)
    
    item = Item.query.get(item_id)
    item.image_thumbnail = thumbnail_image_url

    # Save full image to s3 and get the url
    full_image_key = "{}-800".format(file_key)
    put_object_to_s3(image_bytes=full_image_bytes_stream.getvalue(), filename=full_image_key)
    full_image_url = generate_presigned_url(filename=full_image_key)

    item.image_full = full_image_url

    db.session().commit()
    db.session().close()

    # Remove image from storage after done uploading it to s3

    os.remove(os.path.join(application.config["UPLOAD_FOLDER"], "{}.png".format(file_key)))

def create_thumbnail(img):
    shorter_side = min(img.size)
    horizontal_padding = (shorter_side - img.size[0]) / 2
    vertical_padding = (shorter_side - img.size[1]) / 2
    img = img.crop(
        (
            -horizontal_padding,
            -vertical_padding,
            img.size[0] + horizontal_padding,
            img.size[1] + vertical_padding
        )
    )
    
    img.thumbnail((400, 400))
    return img

def create_full(img):
    img.thumbnail((800, 800))
    return img