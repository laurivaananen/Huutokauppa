from flask import render_template
from application import app
from application.auth.models import AccountInformation

@app.route("/")
def index():
    top_sellers = AccountInformation.top_sellers()
    return render_template("index.html", top_sellers=top_sellers)