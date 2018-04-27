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

`(venv) ~/Huutokauppa$ celery worker -A application -l info`

You need to let the window in which celery is running open. To run the server open up another terminal window and move to the directory, activate the virtual environment and run the application.

`(venv) ~/Huutokauppa$ python run.py`

If the site looks weird try reloading the page by pressing ctrl + shift + r which downloads the css theme from the server and not from browser cache. The css was designed in firefox so it might look different in other browsers.

# Huutokauppa

The application is hosted in AWS Elastic Beanstalk because you can't do certain things in Heroku with the free tier.

[Live version in Heroku (redirects to AWS Elastic Beanstalk)](http://huutokauppa-sovellus.herokuapp.com/)

[Live version in AWS Elastic Beanstalk](http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/)

[Database graph](https://raw.githubusercontent.com/laurivaananen/Huutokauppa/master/documentation/tietokantakaavio.jpg)

[User stories](https://github.com/laurivaananen/Huutokauppa/blob/master/documentation/userstories.md)

# Sovelluksen toiminta

Tällä hetkellä sovelluksessa pystyy:

* Tehdä käyttäjätilin ja kirjautumaan sillä sisään
* Oman käyttäjätilin sivuilla näkee omat tavarat mitä olet laittanut myyntiin sekä omat tavarat mitä olet ostanut.
* Laittaa uuden tavaran kauppaan myyntiin, sekä muokata sen tietoja tai poistaa sen kokonaan
* Selata muiden lisäämiä tavaroita sekä huutaa niitä
* Kun valitsemasi huutamisaika loppuu niin tavara myydään sille kuka oli huutanut eniten. Tai jos kukaan ei ollu huutanut, niin tavara menee pois myynnistä
* Katsoa muiden profiileja
* Etusivulla pystyy tarkkailemaan dataa käyttäjistä
* Admin käyttäjät pystyvät näkemään kaikkien tiedot sekä muokkaamaan, tekemään ja poistamaan niitä.
* Linkki admin paneeliin: http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/admin/
* HUOM! Sinun pitää olla kirjautunut käyttäjällä, jolla on admin oikeudet, jotta näet admin paneelin.
* Sivulla on valmiiksi tehty admin käyttäjä
  * sähköposti: *admin@email.com*
  * salasana: *based_god*
* Admin käyttäjä voi halutessaan antaa muille käyttäjille admin oikeudet