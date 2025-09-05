GymLogger

Sovelluksen toiminnot

Sovelluksessa käyttäjä kirjautuu sisään luomallaan tunnuksella ja aloittaa treenin.
Käyttäjä valitsee tekemänsä harjoitteen (esim. Deadlift) ja valitsee tehtävien työsarjojen määrän ja tavoitteen toistoille (esim. 3 sets, 5 reps). Käyttäjä voi muokata tehtyjä harjoitteita , toistoja, työsarjoja luoden ja lisäten niitä.

Käyttäjä voi lisätä uusia harjoitteita ja lisätä kuvia harjoitteista, mallisuroituksia esim. youtube-linkkien muodossa ja ohjeita harjoitteen tekemisestä. Harjoitteita voi etsiä hakemistosta (esim. Bench Press Barbell) ja niitä voi luokitella (Barbell, Calisthenicss, Machines, Dumbbell). Lempiharjoitteita voi merkata nopeasti löytyviksi ja niistä voi luoda templateja.

Käyttäjäsivuilla näkyy tehdyt treenit ja edistyminen arvioidussa maksimisuorituksessa ((0.033 * reps + 1) * weight) ja paras maksimitoistojen määrä. Tänne käyttäjä voi halutessaan lisätä profiilikuvan. Käyttäjä voi myös exportata datansa jonain taulukkona, ehkä CSV.


Sovelluksen asennus

Asenna flask-kirjasto:

$ pip install flask

Luo tietokannan taulut ja lisää alkutiedot:

$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql

Voit käynnistää sovelluksen näin:

$ flask run

