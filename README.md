# WoimaÄppi
Repositorio Tietokannat ja web-ohjelmointi-kurssin harjoitussovellusta varten.

## Käynnistysohjeet
* Lataa kaikki repositorion tiedostot samaan paikkaan
* Jos latasit tiedostot zippinä, pura tiedostot ja mene Tikawe-main - kansioon

Seuraavat ohjeet ovat Visual Studio Coden terminaalin komentoina. Samat toimivat pieninä muutoksilla myös muissa terminaaleissa.
* asemma virtuaaliympäristö komennolla python3 -m venv venv 
* aktivoi virtuaaliympäristö kommennolla  .\venv\Scripts\Activate.ps1   
* asenna flask-kirjasto: pip install flask
* käynnistä web-sovellus: flask run
* avaa nettiselain ja mene sivulle: http://127.0.0.1:5000/

Repositoriossa on valmiina database.db, jossa muutama rivi syötettynä testaamista varten. Jos tietokantaa tarvitsee muokata tai esim. tyhjentää, se onnistuu lataamalla kansioon sqllite3.exe-sovellus. 
Mukana tulee myös sovelluksen käyttämä SQL-scheema. Sen pystyy lataamaan tyhjään tietokantaan komennolla:  .\sqlite3.exe .\database.db ".read schema.sql"

Sovellusta on testattu näillä tiedostoilla. Saadun palautteen perusteella voi olla tarpeellista muokata Templates-kansion nimi muotoon "templates"

## Lopullisen palautuksen tilanne
Käsitelty palautteen huomiot:
* Poistettu turha import g
* Koodin laatua pyritty parantamaan pylintillä. Kommentit lisätty jokaiseen funktioon.
* Viimeiset tietokantakyselyt siirretty pois app.py:stä pois


## Välipalautuksen 2 tilanne
Käsitelty palautteen huomiot:
* Lisätty käyttäjätunnuksen ja salasanan validointi
* Hajautettu app.py:stä sql-peruskomennot omaan db.py-tiedostoon ja muu tietokantalogiikka data.py, sivujen renderöinti app.py:ssä
* Poistettu turha return funktion new_exercise () lopusta
* Rajattu id-kentät pois käyttäjälle näytettävistä tiedoista

Uudet ominaisuudet:
* Lisätty käyttäjille mahdollisuus määrittää rekisteröinnissä, näyttääkö harjoituksensa julkisina
* Lisätty harjoituksien syöttöön checkbox, näkyykö harjoitus julkisena. Oletusarvo haetaan käyttäjän takaa
* Etusivulle listataan kaikki julkiset harjoitukset
* Lisätty toisijainen tietokohde, eli mahdollisuus kommentoida toisten harjoituksia
* Lisätty tilastosivu

Seuraavassa versiossa (ainakin):
* Ulkoasu kuntoon
* PR-laskenta

## Välipalautuksen 1 tilanne

Tietokantasovellus toteutettu pitkälti kurssin esimerkkisovelluksen pohjalta. Toteutettu useita html-pohjia, joiden rakenne on vielä hyvin pelkistetty. Luotu yksinkertainen sql-relaatiotietokanta, jossa harjoituksiin liittyy harjoiuksen tyyppi (type) ja set/rep-harjoitusluokka (class). Seuraavat luetellut ominaisuudet tuotu sovellukseen. Toisisijaisia tietokohteita ei ole vielä toteuttu, ideana että voisi olla että käyttäjä kommentoida tai "tykätä" toisten käyttäjien harjoituksia.

schema.sql-tiedostossa database.db:n scheema, jos se täytyy ajaa uudestaan. Sqlite3:sta ei ole mukana repositoriossa.

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita (exercises)
* Käyttäjä näkee sovellukseen lisätyt tietokohteet. (exercises ja niihin liitetyt luokat)
* Käyttäjä pystyy etsimään tietokohteita harjoituksen tyypin avulla.
Lisäksi:
* Käyttäjä pystyy valitsemaan tietokohteelle useamman luokittelun (harjoituksen type ja class)

## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. Käyttäjältä kerätään kehonpaino tunnusta perustettaessa.
* Käyttäjä pystyy lisäämään tekemiänsä kuntosaliharjoituksia (pvm, tyyppi, sarjojen määrä, toistojen määrä, paino)
* Käyttäjä näkee sovelluksen laskeman teoreettisen maksipainon (1 RM), joka on laskettu edellisten tehtyjen harjoitusten rullaavana keskiarvona. Enimmäispaino arvioidaan eri sarjatyyppien perusteella joiden perusteella.
* Käyttäjä näkee sovellukseen ehdottoman seuraavan harjoituksen, joka on laskettu % 1 RM:stä. Harjoitus perustuu 2-3 harjoituksen viikkofrekvenssiin, jossa %-tavoite vaihtuu viikoittain.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja aikasarjaa käyttäjän kehityksestä.
* [Lisätty 31.5] Käyttäjä pystyy valitsemaan tietokohteelle useamman luokittelun (harjoituksen type ja clas)
* [Lisätty 14.6] Käyttäjä pystyy valitsemaan tietokohteelle, onko harjoitus julkinen. Käyttäjäprofiilissa on oletusasetus tätä varten.
* [Lisätty 15.6] Käyttäjät pystyvät kommentoimaan toisten käyttäjien harjoituksia sanallisesti