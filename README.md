# OTSO - gym and workout logger

### Sovelluksen toiminnot

Sovelluksessa käyttäjä kirjautuu sisään luomallaan tunnuksella ja aloittaa treenin.

Käyttäjä valitsee haluamansa harjoitteet ja aloittaa treenin. Treeni-sivulla voi valita tehtyjen toistojen määrän sekä vastuksen. Tämän jälkeen treenit voi tallentaa tietokantaan lopettamalla treenin.

Historia -sivulla voi tarkastella tekemiään treenejä ja poistaa niitä tietokannasta.

Tämän lisäksi käyttäjä voi käyttää yhteistä [Body Dysmorphia Feediä](https://en.wikipedia.org/wiki/Body_dysmorphic_disorder), jonne hän voi lisätä kuvia itsestään muiden kommentoitavaksi ja kommentoida muita.


### Sovelluksen asennus

**Asenna flask-kirjasto:**

    $ pip install flask  

**Luo tietokannan taulut ja lisää alkutiedot:**

    $ sqlite3 database.db < schema.sql

**Lisää exercise.json tiedostosta harjoitteet tietokannan tauluun exercises:**

    $ python3 update_exercise.py

**Voit käynnistää sovelluksen näin:**

    $ flask run

Tämän jälkeen luo käyttäjätunnus ja kirjaudu sisään. Begin workout voit hakea ja valita harjoitteita treeniä varten ja aloittaa treenin. Treenin aikana voit merkitä kuinka monta toistoa teet sekä valita vastuksen kilogrammoina. End workout lopettaa treenin ja lisää treenin tietokantaan. Workout history näyttää menneet treenit.

