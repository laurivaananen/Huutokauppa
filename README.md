# Huutokauppa

## TODO
Add a database container

## Installing and running the application locally

This application uses sqlite, redis and python 3.6.3.

Download redis: `sudo apt install redis-server`

Check python version: `python -V` or `python3 -V`

Download the zip or clone this repository to your computer.

First we need to create a virtual environment and download required packages.

```
~/Huutokauppa$ python -m venv venv
~/Huutokauppa$ source venv/bin/activate
(venv) ~/Huutokauppa$ pip install -r requirements.txt
```

Next we need to start celery which works as a message queue for our application

`(venv) ~/Huutokauppa$ celery worker -A application -l info`

You need to let the window in which celery is running open. To run the server open up another terminal window and move to the directory, activate the virtual environment and run the application.

`(venv) ~/Huutokauppa$ python run.py`

If the site looks weird try reloading the page by pressing ctrl + shift + r which downloads the css theme from the server and not from browser cache. The css was designed in firefox so it might look different in other browsers.

## Links

The application is hosted in AWS Elastic Beanstalk because you can't do certain things in Heroku with the free tier.

[Live version in Heroku (redirects to AWS Elastic Beanstalk)](http://huutokauppa-sovellus.herokuapp.com/)

[Live version in AWS Elastic Beanstalk](http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/)

[Database graph](https://raw.githubusercontent.com/laurivaananen/Huutokauppa/master/documentation/kaavio_uusi.jpg)

[User stories](https://github.com/laurivaananen/Huutokauppa/blob/master/documentation/userstories.md)

## Features

* Responsive UI
* You can create, edit and delete a user account
* In you account page you can see your items that are currently on sale and all the items that you have bought
* When adding a new item to sale you can choose name, starting price, bidding end datetime, image, description, category and quality
* You can edit the item information or delete the item
* On items detail page is also a list of other items being sold by the seller
* When your chosen bidding time ends the item gets sold to the highest bidder, or removed from the store if nobody bid on it
* When looking at other profiles you can only see limited information (no billing address or purchase history)
* On the index page you can see users based on the amount of bids and amounts of items they have sold
* On the index page you have a list of top 4 most bid items currently on sale
* You can sort items based on price, bidding time left, date added to sale or name
* You can sort items based on their category or quality
* Full admin paned at http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/admin/
* Your account needs to have admin priviledges to see the admin panel. Only another admin can give admin priviledges
* Admins can delete users and items or edit their information
* Admins can add new product categories and product qualities
* There is a default admin account
  * email address: admin@email.com
  * password: based_god
