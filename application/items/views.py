from application import application, db
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from application.items.models import Item, Quality
from application.items.forms import ItemForm
from application.items.tasks import sell_item, delete_task, image_to_s3, create_thumbnail, create_full
from application.extensions import get_or_create, put_object_to_s3
from application.bid.forms import BidForm
from application.bid.models import Bid
import datetime
from pytz import utc
import pytz
from werkzeug.utils import secure_filename
import os
from PIL import Image
from io import BytesIO
from werkzeug.exceptions import RequestEntityTooLarge

@application.route("/items/", methods=["GET"])
def items_index():
    item_count = Item.query.filter_by(sold=False, hidden=False).count()
    return render_template("items/list.html", item_count=item_count, next_page=1)

@application.route("/loaditems")
def load_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.filter_by(sold=False, hidden=False).order_by(Item.bidding_end.asc()).paginate(page, 8, error_out=False)

    next_page = None
    if items.has_next:
        next_page = items.next_num

    return jsonify(items=[{"name": item.name,
                           "image_url": item.image_thumbnail_url(),
                           "starting_price": item.starting_price,
                           "id": item.id,
                           "latest_bid": item.bid_latest(item.id),
                           "bidding_time_left": item.bidding_time_left(),
                           "bidding_end": item.datetime_from_utc(),
                           "quality": item.quality.name,
                           "seller": item.account_information.user_account.user_name,
                           "seller_id": item.account_information_id} for item in items.items],
                           next_page=next_page)


@application.route("/items/new/")
@login_required
def items_form():
    form = ItemForm()
    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]
    return render_template("items/new.html", form = form)

@application.route("/items/<item_id>/", methods=["GET"])
def item_detail(item_id):

    item = Item.query.get_or_404(item_id)
    bids = Bid.query.filter_by(item_id=item_id).order_by(Bid.amount.desc()).limit(15)

    return render_template("items/detail.html", item=item, form=BidForm(), bids=bids)

@login_required
@application.route("/items/edit/<item_id>/", methods=["GET"])
def item_edit(item_id):

    item = Item.query.get(item_id)

    form = ItemForm(obj=item)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not item.sold and not item.hidden:
        if current_user.id is item.account_information_id:
            return render_template("items/edit.html", item=item, form=form)
        else:
            return redirect(url_for('items_index'))

    else:
        return redirect(url_for('items_index'))

@login_required
@application.route("/items/update/<item_id>/", methods=["POST"])
def item_update(item_id):

    form = ItemForm(request.form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not (form.name.validate(form) and (form.description.validate(form)) and (form.quality.validate(form))):
        return render_template("items/edit.html", form=form, item=Item.query.get(item_id))

    item = Item.query.get_or_404(item_id)
    if not item.sold and not item.hidden:
        if current_user.id == item.account_information.id:
            
            item.name = form.name.data

            item.description = form.description.data

            item.quality_id = form.quality.data

            db.session().commit()

    return redirect(url_for("item_detail", item_id=item.id))

@application.route("/items/delete/<item_id>/", methods=["POST"])
@login_required
def item_delete(item_id):

    item = Item.query.get(item_id)
    if not item.sold and not item.hidden:
        if current_user.id == item.account_information.id:
            # Revoking the selling task of this item when deleted
            delete_task(item.celery_task_id)
            db.session().delete(item)
            db.session().commit()

    return redirect(url_for("items_index"))

@application.route("/items/", methods=["POST"])
@login_required
def items_create():
    form = ItemForm(request.form)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not form.validate_on_submit():
        return render_template("items/new.html", form=form)

    if 'image' not in request.files:
        form.image.errors.append("No image found")
        return render_template("items/new.html", form=form)

    image_file = request.files.get("image")

    if image_file.filename.rsplit(".", 1)[1].lower() not in ["jpg", "jpeg", "png", "bmp"]:
        form.image.errors.append("Invalid filetype")
        return render_template("items/new.html", form=form)

    helsinki = pytz.timezone("Europe/Helsinki")
    
    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)

    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")

    bidding_end = helsinki.localize(bidding_end)

    bidding_end = bidding_end.astimezone(utc)



    img = Image.open(request.files.get("image"))

    sec_filename = secure_filename(image_file.filename)
    timecode = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_key = "{}-{}".format(sec_filename.rsplit(".", 1)[0], timecode)


    sec_filename = secure_filename(img.filename)
    timecode = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_key = "{}-{}".format(sec_filename.rsplit(".", 1)[0], timecode)

    thumbnail_image_key = "{}-400".format(file_key)
    full_image_key = "{}-800".format(file_key)

    thumbnail_image_name = "{}.jpg".format(thumbnail_image_key)
    full_image_name = "{}.jpg".format(full_image_key)





    thumbnail_image = create_thumbnail(img)
    full_image = create_full(img)

    thumbnail_image = thumbnail_image.convert('RGB')
    thumbnail_image_bytes_stream = BytesIO()
    thumbnail_image.save(thumbnail_image_bytes_stream, "JPEG", quality=70)

    full_image = full_image.convert('RGB')
    full_image_bytes_stream = BytesIO()
    full_image.save(full_image_bytes_stream, "JPEG", quality=75)

    if os.environ.get("AWS") == "huutokauppa-sovellus":
        # Save thumbnail image to s3 and get the url
        # thumbnail_image_key = thumbnail_image_key
        put_object_to_s3(image_bytes=thumbnail_image_bytes_stream.getvalue(), filename=thumbnail_image_key)
        # thumbnail_image_url = generate_presigned_url(filename=thumbnail_image_key)
        thumbnail_image_url = "{}{}".format(application.config["S3_LOCATION"], thumbnail_image_key)

        # Save full image to s3 and get the url
        # full_image_key = full_image_key
        put_object_to_s3(image_bytes=full_image_bytes_stream.getvalue(), filename=full_image_key)
        # full_image_url = generate_presigned_url(filename=full_image_key)
        full_image_url = "{}{}".format(application.config["S3_LOCATION"], full_image_key)
    else:
        with open(os.path.join(application.config["UPLOAD_FOLDER"], thumbnail_image_name), "wb") as f:
            f.write(thumbnail_image_bytes_stream.getvalue())
            thumbnail_image_url = url_for('static', filename="images/{}".format(thumbnail_image_name))

        with open(os.path.join(application.config["UPLOAD_FOLDER"], full_image_name), "wb") as f:
            f.write(full_image_bytes_stream.getvalue())
            full_image_url = url_for('static', filename="images/{}".format(full_image_name))


    # item = Item.query.get(item_id)
    # item.image_thumbnail = thumbnail_image_url
    # item.image_full = full_image_url

    # db.session().commit()
    # db.session().close()








    # img = img.convert('RGB')
    # bytes_stream = BytesIO()
    # img.save(bytes_stream, "PNG")

    
        
    # with open(os.path.join(application.config["UPLOAD_FOLDER"], "{}.png".format(file_key)), "wb") as f:
    #     f.write(bytes_stream.getvalue())

    # Showing image from storage while it's being uploaded to s3
    # image_url = url_for('static', filename="images/{}".format("{}.png".format(file_key)))

    item = Item(starting_price = form.starting_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = form.quality.data,
                description = form.description.data,
                bidding_end = bidding_end,
                image_thumbnail = thumbnail_image_url,
                image_full = full_image_url)

    db.session().add(item)
    db.session().flush()

    # Using a background task to upload image to s3, otherwise the user has to wait
    # if os.environ.get("AWS") == "huutokauppa-sovellus":
    #     image_to_s3.apply_async(args=[file_key, item.id])

    # Getting the id of a celery task that will sell this item
    print(item.id)
    task_id = sell_item.apply_async(args=[item.id], eta=bidding_end)
    item.celery_task_id = task_id.id
    db.session().commit()

    return redirect(url_for("item_detail", item_id=item.id))
