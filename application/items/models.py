from application import db
from application.models import Base
from sqlalchemy.sql import text

class Item(Base):

    __tablename__ = 'Item'

    starting_price = db.Column(db.Integer, nullable=False)
    buyout_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(4096), nullable=False)
    bidding_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    bidding_end = db.Column(db.Date, nullable=False)

    def get_bidding_end(self):
        from datetime import datetime
        return self.bidding_end.strftime("%Y-%m-%d")

    hidden = db.Column(db.Boolean, default=False)
    sold = db.Column(db.Boolean, nullable=False)

    quality = db.Column(db.Integer(), db.ForeignKey("Quality.id"), nullable=False)

    images = db.relationship("Image", backref='Item', lazy=True)

    bids = db.relationship("Bid", backref='Item', lazy=True)

    account_information_id = db.Column(db.Integer, db.ForeignKey('AccountInformation.id'), nullable=False)

    def __init__(self, name, buyout_price, starting_price, quality, description, bidding_end, account_information_id):
        self.name = name
        self.buyout_price = buyout_price
        self.starting_price = starting_price
        self.sold = False
        self.account_information_id = account_information_id
        self.quality = quality
        self.description = description
        self.bidding_end = bidding_end

    @staticmethod
    def bid_latest(item_id):
        stmt = text("SELECT MAX(Bid.amount) AS bid_latest FROM Item"
                    " INNER JOIN Bid on Bid.item_id = Item.id"
                    " WHERE Item.id = :item_id;").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = res.fetchone()

        if response["bid_latest"] is None:
            stmt = text("SELECT Item.starting_price AS starting_price FROM Item"
                        " WHERE Item.id = :item_id;").params(item_id=item_id)

            res = db.engine.execute(stmt)

            response = res.fetchone()
            return response["starting_price"]

        return response["bid_latest"]

    @staticmethod
    def bid_order(item_id):
        stmt = text("SELECT Bid.amount AS amount, UserAccount.user_name AS user_name, Bid.date_created AS date_created FROM Item"
                    " INNER JOIN Bid ON Bid.item_id = Item.id"
                    " INNER JOIN AccountInformation ON Bid.account_information_id = AccountInformation.id"
                    " INNER JOIN UserAccount ON UserAccount.account_information = AccountInformation.id"
                    " WHERE Item.id = :item_id;"
                    " ORDER BY Bid.amount DESC").params(item_id=item_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"amount":row["amount"], "user_name":row["user_name"], "date_created":row["date_created"]})

        return response

class Image(Base):

    __tablename__ = "Image"

    file_path = db.Column(db.String(144), nullable=False)

    item = db.Column(db.Integer, db.ForeignKey('Item.id'), nullable=False)

    def __init__(self, file_path, item):
        self.file_path = file_path
        self.item = item


class Quality(Base):

    __tablename__ = "Quality"

    name = db.Column(db.String(144), nullable=False)

    items = db.relationship("Item", backref="Quality", lazy=True)

    def __init__(self, name):
        self.name = name
