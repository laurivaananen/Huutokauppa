from application import application, db
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from application.items.models import Item, Quality, Category
from application.items.forms import ItemForm, ItemSortForm
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
    # Items are loaded using ajax
    item_count = Item.query.filter_by(sold=False, hidden=False).count()
    item_sort_form = ItemSortForm()

    qualities = Quality.query.all()
    item_sort_form.quality.choices = [(quality.id, quality.name) for quality in qualities]
    item_sort_form.quality.choices.insert(0, (0, "All"))

    categories = Category.query.all()
    item_sort_form.category.choices = [(category.id, category.name) for category in categories]
    item_sort_form.category.choices.insert(0, (0, "All"))
    return render_template("items/list.html", item_count=item_count, form=item_sort_form)

@application.route("/loaditems", methods=["POST", "GET"])
def load_items():
    # The javascript in items/list.html calls this function
    form = ItemSortForm(request.form)

    key = form.key.data
    page = int(form.page.data)
    quality = form.quality.data
    category = form.category.data
    direction = form.direction.data

    try:
        keys = {1: Item.current_price, 2: Item.bidding_end, 3: Item.bidding_start, 4: Item.name}
        obj = keys[key]
        directions = {1: obj.asc(), 2: obj.desc()}
        order = directions[direction]
    except KeyError:
        order = Item.bidding_end.asc()

    qualities_count = Quality.query.count()
    quality_in = [quality]
    if quality == 0:
        quality_in = [x for x in range(1, qualities_count + 1)]

    # Filter items if category_id is not in category_in
    categories_count = Category.query.count()
    category_in = [category]
    # If selected 0 (All) don't filter by category
    if category == 0:
        category_in = [x for x in range(1, categories_count + 1)]

    items = Item.query.filter(Item.sold==False,
                              Item.hidden==False,
                              Item.quality_id.in_(quality_in),
                              Item.category_id.in_(category_in)).order_by(order)

    item_count = len(items.all())
    # Returning 6 items per page
    items = items.paginate(page, 6, error_out=True)

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
                   next_page=next_page,
                   item_count=item_count)


@application.route("/items/new/")
@login_required
def items_form():
    form = ItemForm()
    # Adding qualities and categories manually to the form
    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]
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

    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if not item.sold and not item.hidden:
        if current_user.is_authenticated() and (current_user.id is item.account_information_id):
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

    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    # Validating only certain fields from the form
    if not (form.name.validate(form) and (form.description.validate(form)) and (form.quality.validate(form))):
        return render_template("items/edit.html", form=form, item=Item.query.get(item_id))

    item = Item.query.get_or_404(item_id)
    if not item.sold and not item.hidden:
        if current_user.is_authenticated() and (current_user.id == item.account_information.id):
            
            item.name = form.name.data
            item.description = form.description.data
            item.quality_id = form.quality.data
            item.category_id = form.category.data
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

    # Fetching all qualities from the database and manually adding them to the form
    qualities = Quality.query.all()
    form.quality.choices = [(quality.id, quality.name) for quality in qualities]

    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]

    if not form.validate_on_submit():
        return render_template("items/new.html", form=form)

    helsinki = pytz.timezone("Europe/Helsinki")
    bidding_end = "{} {}".format(form.bidding_end.bidding_end_date.data, form.bidding_end.bidding_end_time.data)
    bidding_end = datetime.datetime.strptime(bidding_end, "%Y-%m-%d %H:%M")
    bidding_end = helsinki.localize(bidding_end)
    # Saving datetime in UTC timezone for easier processing
    bidding_end = bidding_end.astimezone(utc)


    if 'image' not in request.files:
        form.image.errors.append("No image found")
        return render_template("items/new.html", form=form)

    image_file = request.files.get("image")

    # If not image file return form
    if image_file.filename.rsplit(".", 1)[1].lower() not in ["jpg", "jpeg", "png", "bmp"]:
        form.image.errors.append("Invalid filetype")
        return render_template("items/new.html", form=form)


    img = Image.open(request.files.get("image"))

    sec_filename = secure_filename(image_file.filename)
    timecode = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_key = "{}-{}".format(sec_filename.rsplit(".", 1)[0], timecode)

    thumbnail_image_key = "{}-400".format(file_key)
    full_image_key = "{}-800".format(file_key)

    thumbnail_image_name = "{}.jpg".format(thumbnail_image_key)
    full_image_name = "{}.jpg".format(full_image_key)

    # Image filename format: name-timestamp-size
    thumbnail_image = create_thumbnail(img)
    full_image = create_full(img)

    thumbnail_image = thumbnail_image.convert('RGB')
    thumbnail_image_bytes_stream = BytesIO()
    thumbnail_image.save(thumbnail_image_bytes_stream, "JPEG", quality=70)

    full_image = full_image.convert('RGB')
    full_image_bytes_stream = BytesIO()
    full_image.save(full_image_bytes_stream, "JPEG", quality=75)

    if os.environ.get("AWS") == "huutokauppa-sovellus":
        # Save thumbnail image to s3
        put_object_to_s3(image_bytes=thumbnail_image_bytes_stream.getvalue(), filename=thumbnail_image_key)
        thumbnail_image_url = "{}{}".format(application.config["S3_LOCATION"], thumbnail_image_key)

        # Save full image to s3
        put_object_to_s3(image_bytes=full_image_bytes_stream.getvalue(), filename=full_image_key)
        full_image_url = "{}{}".format(application.config["S3_LOCATION"], full_image_key)
    else:
        # If running locally save images to static/images
        with open(os.path.join(application.config["UPLOAD_FOLDER"], thumbnail_image_name), "wb") as f:
            f.write(thumbnail_image_bytes_stream.getvalue())
            thumbnail_image_url = url_for('static', filename="images/{}".format(thumbnail_image_name))

        with open(os.path.join(application.config["UPLOAD_FOLDER"], full_image_name), "wb") as f:
            f.write(full_image_bytes_stream.getvalue())
            full_image_url = url_for('static', filename="images/{}".format(full_image_name))

    item = Item(starting_price = form.starting_price.data,
                current_price = form.starting_price.data,
                name = form.name.data,
                account_information_id = current_user.id,
                quality = form.quality.data,
                category = form.category.data,
                description = form.description.data,
                bidding_end = bidding_end,
                image_thumbnail = thumbnail_image_url,
                image_full = full_image_url)


    db.session().add(item)
    db.session().flush()

    # Adding a new task for the item that sells it when the bidding time ends
    task_id = sell_item.apply_async(args=[item.id], eta=bidding_end)
    item.celery_task_id = task_id.id
    db.session().commit()

    return redirect(url_for("item_detail", item_id=item.id))
