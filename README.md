# Installing and running the application locally

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

`(venv) ~/Huutokauppa$ celery -A application worker -l info -E`

You need to let the window in which celery is running open. To run the server open up another terminal window and move to the directory, activate the virtual environment and run the application.

`(venv) ~/Huutokauppa$ python run.py`

# Huutokauppa

The application is hosted in AWS Elastic Beanstalk because you can't do certain things in Heroku with the free tier.

[Live version in Heroku (redirects to AWS Elastic Beanstalk)](http://huutokauppa-sovellus.herokuapp.com/)

[Live version in AWS Elastic Beanstalk](http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/)

[Database graph](https://raw.githubusercontent.com/laurivaananen/Huutokauppa/master/documentation/tietokantakaavio.jpg)

[User stories](https://github.com/laurivaananen/Huutokauppa/blob/master/documentation/userstories.md)

#cd Sovelluksen toiminta

Tällä hetkellä sovelluksessa pystyy:

* Tehdä käyttäjätilin ja kirjautumaan sillä sisään
* Laittaa uuden tavaran kauppaan myyntiin, sekä muokata sen tietoja tai poistaa sen kokonaan
* Kun valitsemase huutamisaika loppuu niin tavara myydään (tämä ominaisuus toimii vielä vain lokaalissa versiossa)
* Selata muiden lisäämiä tavaroita sekä huutamaan niitä
* Katsoa muiden profiileja
* Lisätä omaan käyttäjätiliin rahaa(rahalla ei tällä hetkellä voi tehdä vielä mitään)
* Etusivulla pystyy tarkkailemaan dataa käyttäjistä