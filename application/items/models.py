from application import db

class Item(db.Model):

    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

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

    quality_id = db.Column(db.Integer(), db.ForeignKey("Quality.id"), nullable=False)

    images = db.relationship("Image", backref='Item', lazy=True)

    account_information_id = db.Column(db.Integer, db.ForeignKey('AccountInformation.id'), nullable=False)

    def __init__(self, name, buyout_price, starting_price, quality_id, description, bidding_end, account_information_id):
        self.name = name
        self.buyout_price = buyout_price
        self.starting_price = starting_price
        self.sold = False
        self.account_information_id = account_information_id
        self.quality_id = quality_id
        self.description = description
        self.bidding_end = bidding_end

class Image(db.Model):

    __tablename__ = "Image"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(144), nullable=False)

    item = db.Column(db.Integer, db.ForeignKey('Item.id'), nullable=False)

    def __init__(self, file_path, item):
        self.file_path = file_path
        self.item = item


class Quality(db.Model):

    __tablename__ = "Quality"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)

    items = db.relationship("Item", backref="Quality", lazy=True)

    def __init__(self, name):
        self.name = name
