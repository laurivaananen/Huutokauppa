from application import db
from application.models import Base
from sqlalchemy.sql import text
from flask import url_for
import datetime
import pytz
import os

class Item(Base):

    __tablename__ = 'item'

    starting_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(4096), nullable=False)
    bidding_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    bidding_end = db.Column(db.DateTime, nullable=False)
    hidden = db.Column(db.Boolean, default=False)
    sold = db.Column(db.Boolean, nullable=False)

    image = db.Column(db.String(128))

    quality_id = db.Column(db.Integer(), db.ForeignKey("quality.id"), nullable=False)

    bids = db.relationship("Bid", backref='item', lazy=True, cascade="all, delete-orphan")

    account_information_id = db.Column(db.Integer, db.ForeignKey("account_information.id"))

    account_information = db.relationship("AccountInformation", back_populates="items", foreign_keys="Item.account_information_id")

    buyer_account_information_id = db.Column(db.Integer, db.ForeignKey('account_information.id'))

    buyer_account_information = db.relationship("AccountInformation", back_populates="bought_items", foreign_keys="Item.buyer_account_information_id")

    celery_task_id = db.Column(db.String(92))

    def __init__(self, name, starting_price, quality, description, bidding_end, account_information_id, image):
        self.name = name
        self.starting_price = starting_price
        self.sold = False
        self.account_information_id = account_information_id
        self.quality_id = quality
        self.description = description
        self.bidding_end = bidding_end
        self.image = image

    def image_url(self):
        # if os.environ.get("AWS") == "huutokauppa-sovellus":
        return self.image

        # return url_for('static', filename="images/{}".format(self.image))

    def datetime_from_utc(self):
        helsinki = pytz.timezone("Europe/Helsinki")

        bidding_end_utc = pytz.utc.localize(self.bidding_end)

        return bidding_end_utc.astimezone(helsinki).strftime("%Y-%m-%d %H:%M")

    def bidding_time_left(self):
        import math
        time_now = pytz.utc.localize(datetime.datetime.utcnow())
        bidding_time_end = pytz.utc.localize(self.bidding_end)
        time_difference = bidding_time_end - time_now
        time_difference_seconds = int(math.floor(time_difference.total_seconds()))

        time_left_hour = time_difference_seconds

        hour = datetime.timedelta(hours=1)
        time_difference_hours = 0
        time_difference_minutes = 0
        if(time_difference_seconds > hour.seconds):
            time_left_hour = time_difference_seconds % hour.seconds

            time_difference_round = time_difference_seconds - time_left_hour
            time_difference_hours = int(time_difference_round / hour.seconds)

        time_left_minute = time_left_hour

        minute = datetime.timedelta(minutes=1)
        if(time_left_hour > minute.seconds):

            time_left_minute = time_left_hour % minute.seconds

            time_difference_round = time_left_hour - time_left_minute
            time_difference_minutes = int(time_difference_round / minute.seconds)

        time_difference_seconds = time_left_minute

        return {"hours": time_difference_hours, "minutes": time_difference_minutes, "seconds": time_difference_seconds}

    @staticmethod
    def highest_bid(item_id):
        stmt = text("SELECT bid.id AS bid_id, bid.amount, bid.account_information_id, bid.item_id FROM item"
                    " INNER JOIN bid ON bid.item_id = item.id"
                    " WHERE item.id = :item_id"
                    " ORDER BY bid.amount DESC").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = res.fetchone()

        if response:
            return response["bid_id"]

        return None

    def latest_bid(self):
        stmt = text("SELECT MAX(bid.amount) AS bid_latest FROM item"
                    " INNER JOIN bid ON bid.item_id = item.id"
                    " WHERE item.id = :item_id;").params(item_id=self.id)

        res = db.engine.execute(stmt)

        response = res.fetchone()

        return response["bid_latest"]


    @staticmethod
    def bid_latest(item_id):
        stmt = text("SELECT MAX(bid.amount) AS bid_latest FROM item"
                    " INNER JOIN bid ON bid.item_id = item.id"
                    " WHERE item.id = :item_id;").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = res.fetchone()

        if response["bid_latest"] is None:
            stmt = text("SELECT item.starting_price AS starting_price FROM item"
                        " WHERE item.id = :item_id;").params(item_id=item_id)

            res = db.engine.execute(stmt)

            response = res.fetchone()
            return response["starting_price"]

        return response["bid_latest"]

    @staticmethod
    def bid_order(item_id):
        stmt = text("SELECT bid.amount AS amount, user_account.user_name AS user_name, bid.date_created AS date_created FROM item"
                    " INNER JOIN bid ON bid.item_id = item.id"
                    " INNER JOIN account_information ON bid.account_information_id = account_information.id"
                    " INNER JOIN user_account ON user_account.account_information_id = account_information.id"
                    " WHERE item.id = :item_id"
                    " ORDER BY bid.amount ASC").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"amount":row["amount"], "user_name":row["user_name"], "date_created":row["date_created"]})

        return response

class Quality(Base):

    __tablename__ = "quality"

    name = db.Column(db.String(144), nullable=False)

    items = db.relationship("Item", backref="quality", lazy=True, uselist=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
