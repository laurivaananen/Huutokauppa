# Installing and running the application locally

This application uses sqlite and redis.

Download redis: `sudo apt install redis-server`

Once you have installed requirements open up another terminal window and activate the virtual environment. Then run this command to start celery task queue `celery -A application worker -l info -E`

The application is hosted in AWS Elastic Beanstalk because you can't do certain things in Heroku with the free tier.

# Huutokauppa

[Live version in Heroku (redirects to AWS Elastic Beanstalk)](http://huutokauppa-sovellus.herokuapp.com/)

[Live version in AWS Elastic Beanstalk](http://huutokauppa-sovellus.us-west-2.elasticbeanstalk.com/)

[Database graph](https://raw.githubusercontent.com/laurivaananen/Huutokauppa/master/documentation/tietokantakaavio.jpg)

[User stories](https://github.com/laurivaananen/Huutokauppa/blob/master/documentation/userstories.md)

## Sovelluksen toiminta

Jos sovelluksen ulkoasu näyttää oudolta paina ctrl + shift + r.
 Tällöin selain lataa ulkoasun serveriltä eikä välimuistista.

Tällä hetkellä sovelluksessa pystyy:

* Tehdä käyttäjätilin ja kirjautumaan sillä sisään
* Laittaa uuden tavaran kauppaan myyntiin, sekä muokata sen tietoja tai poistaa sen kokonaan
* Kun valitsemase huutamisaika loppuu niin tavara myydään (tämä ominaisuus toimii vielä vain lokaalissa versiossa ei AWS)
* Selata muiden lisäämiä tavaroita sekä huutamaan niitä
* Katsoa muiden profiileja
* Lisätä omaan käyttäjätiliin rahaa(rahalla ei tällä hetkellä voi tehdä vielä mitään)
* Etusivulla pystyy tarkkailemaan dataa käyttäjistä