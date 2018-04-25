from application import db
from application.models import Base
from sqlalchemy.sql import text
import datetime
import pytz

class Item(Base):

    __tablename__ = 'item'

    starting_price = db.Column(db.Integer, nullable=False)
    buyout_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(4096), nullable=False)
    bidding_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    bidding_end = db.Column(db.DateTime, nullable=False)

    def get_bidding_end(self):
        from datetime import datetime
        return self.bidding_end.strftime("%Y-%m-%d")

    hidden = db.Column(db.Boolean, default=False)
    sold = db.Column(db.Boolean, nullable=False)

    quality_id = db.Column(db.Integer(), db.ForeignKey("quality.id"), nullable=False)

    images = db.relationship("Image", backref='item', lazy=True)

    bids = db.relationship("Bid", backref='item', lazy=True)

    account_information_id = db.Column(db.Integer, db.ForeignKey("account_information.id"))

    account_information = db.relationship("AccountInformation", back_populates="items", foreign_keys="Item.account_information_id")

    buyer_account_information_id = db.Column(db.Integer, db.ForeignKey('account_information.id'))

    buyer_account_information = db.relationship("AccountInformation", back_populates="bought_items", foreign_keys="Item.buyer_account_information_id")

    def __init__(self, name, buyout_price, starting_price, quality, description, bidding_end, account_information_id):
        self.name = name
        self.buyout_price = buyout_price
        self.starting_price = starting_price
        self.sold = False
        self.account_information_id = account_information_id
        self.quality_id = quality
        self.description = description
        self.bidding_end = bidding_end

    def datetime_from_utc(self):
        helsinki = pytz.timezone("Europe/Helsinki")

        bidding_end_utc = pytz.utc.localize(self.bidding_end)

        return bidding_end_utc.astimezone(helsinki).strftime("%Y-%m-%d %H:%M")

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
                    " ORDER BY bid.amount DESC").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"amount":row["amount"], "user_name":row["user_name"], "date_created":row["date_created"]})

        return response

class Image(Base):

    __tablename__ = "image"

    file_path = db.Column(db.String(144), nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self, file_path, item):
        self.file_path = file_path
        self.item_id = item


class Quality(Base):

    __tablename__ = "quality"

    name = db.Column(db.String(144), nullable=False)

    items = db.relationship("Item", backref="quality", lazy=True, uselist=False)

    def __init__(self, name):
        self.name = name
