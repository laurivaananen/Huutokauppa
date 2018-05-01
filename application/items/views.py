from application import application, db
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from application.items.models import Item, Quality
from application.items.forms import ItemForm
from application.items.tasks import sell_item, delete_task
from application.extensions import get_or_create, upload_file_to_s3, put_object_to_s3, generate_presigned_url
from application.bid.forms import BidForm
from application.bid.models import Bid
import datetime
from pytz import utc
import pytz
from werkzeug.utils import secure_filename
import os
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
                           "image_url": item.image_url(),
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
    # print("\n\n\n")
    # print(item.celery_result)
    # print(item.celery_result.status)
    # print(item.celery_result.id)
    # delete_task("16cc435c-7812-431e-b244-b68f6fcb3f01")

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

    # if form.validate_on_submit():
    #     image_data = form.image.data
    #     print("\n\n")
    #     print(image_data)

    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    if not form.validate_on_submit():
        return render_template("items/new.html", form=form)

    if 'image' not in request.files:
        form.image.errors.append("No image found")
        return render_template("items/new.html", form=form)

    image_file = request.files.get("image")
    print("\n\n")
    print(image_file)

    if image_file.filename.rsplit(".", 1)[1].lower() not in ["jpg", "jpeg", "png", "bmp"]:
        form.image.errors.append("Invalid filetype")
        return render_template("items/new.html", form=form)

    helsinki = pytz.timezone("Europe/Helsinki")

    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)

    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")

    bidding_end = helsinki.localize(bidding_end)

    bidding_end = bidding_end.astimezone(utc)

    sec_filename = secure_filename(image_file.filename)

    timecode = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    filename = "{}-{}.{}".format(sec_filename.rsplit(".", 1)[0], timecode, sec_filename.rsplit(".", 1)[1])

    # sec_file_key = secure_filename(form.image)
    # print(sec_file_key)
    image_bytes = form.image.data
    print("\n\nGOT IMAGE BYTES")
    print(image_bytes)
    if image_bytes:
        print("SUCCESS")
        print(image_bytes)

    image_bytes = request.files.get("image")

    file_key = "{}-{}".format(sec_filename, timecode)

    image_file.save(os.path.join(application.config["UPLOAD_FOLDER"], filename))

    put_object_to_s3(image_bytes=image_bytes, filename=file_key)
    # output = upload_file_to_s3(image_file, application.config["S3_BUCKET"], filename=filename)
    print("\n\n\n")

    s3_image_url = generate_presigned_url(filename=file_key)

    print("\n\n")
    print(s3_image_url)

    item = Item(starting_price = form.starting_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = form.quality.data,
                description = form.description.data,
                bidding_end = bidding_end,
                image = filename)

    db.session().add(item)
    db.session().flush()
    # Getting the id of a celery task that will sell this item
    print(item.id)
    task_id = sell_item.apply_async(args=[item.id], eta=bidding_end)
    item.celery_task_id = task_id.id
    db.session().commit()

    return redirect(url_for("items_index"))
