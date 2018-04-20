from flask import render_template
from application import application
from application.auth.models import AccountInformation

@application.route("/")
def index():
    top_sellers = AccountInformation.top_sellers()
    top_bidders = AccountInformation.top_bidders()
    return render_template("index.html", top_sellers=top_sellers, top_bidders=top_bidders)