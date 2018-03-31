# Huutokauppa

[Live version in Heroku](http://huutokauppa-sovellus.herokuapp.com/)

[Database graph](https://yuml.me/cdb203f6.jpg)

[User stories](https://github.com/laurivaananen/Huutokauppa/blob/master/documentation/userstories.md)

## Sovelluksen käyttäjiä

Ostaja
* Voi tehdä tarjouksia eri tuotteista
* Voi tallettaa rahaa tililleen
* Voi selata eri tuotteita kategorioittain

Myyjä
* Voi laittaa eri tuotteita myyntiin
* Voi muuttaa omien tuotteidensa tietoja kuten kuva, nimi ja kuvaus

Admin
* Pystyy poistamaan käyttäjiä palvelusta
* Pystyy poistamaan eri tuotteita

## Sovelluksen toiminta

Jos olet myyjä, voit lisätä omia tuotteitasi sivulle myyntiin. Ostajat voivat tarjota tuotteesta jonkun hinnan niin kauan, kuin tuote on myynnissä. Korkeimman hinnan tarjoaja saa tuotteen. Adminit voivat seurata sivun toimintaa ja tarpeen tullessa poistaa käyttäjiä tai tuotteita sivulta.
