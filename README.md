# WoimaÄppi
Repositorio Tietokannat ja web-ohjelmointi-kurssin harjoitussovellusta varten 
## Välipalautuksen 1 tilanne

Tietokantasovellus toteutettu pitkälti kurssin esimerkkisovelluksen pohjalta. Toteutettu useita html-pohjia, joiden rakenne on vielä hyvin pelkistetty. Luotu yksinkertainen sql-relaatiotietokanta, jossa harjoituksiin liittyy harjoiuksen tyyppi (type) ja set/rep-harjoitusluokka (class). Seuraavat ominaisuudet tuotu sovellukseen. Toisisijaisia tietokohteita ei ole vielä toteuttu, ideana että voisi olla että käyttäjä kommentoida tai "tykätä" toisten käyttäjien harjoituksia.

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita (exercises)
* Käyttäjä näkee sovellukseen lisätyt tietokohteet.
* Käyttäjä pystyy etsimään tietokohteita harjoituksen tyypin avulla.
Lisäksi:
* Käyttäjä pystyy valitsemaan tietokohteelle useamman luokittelun (harjoituksen type ja clas)

## Sovelluksen toiminnot
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. Käyttäjältä kerätään kehonpaino tunnusta perustettaessa.
* Käyttäjä pystyy lisäämään tekemiänsä kuntosaliharjoituksia (pvm, tyyppi, sarjojen määrä, toistojen määrä, paino)
* Käyttäjä näkee sovelluksen laskeman teoreettisen maksipainon (1 RM), joka on laskettu edellisten tehtyjen harjoitusten rullaavana keskiarvona. Enimmäispaino arvioidaan eri sarjatyyppien perusteella joiden perusteella.
* Käyttäjä näkee sovellukseen ehdottoman seuraavan harjoituksen, joka on laskettu % 1 RM:stä. Harjoitus perustuu 2-3 harjoituksen viikkofrekvenssiin, jossa %-tavoite vaihtuu viikoittain.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja aikasarjaa käyttäjän kehityksestä.
* [Lisätty 31.5] Käyttäjä pystyy valitsemaan tietokohteelle useamman luokittelun (harjoituksen type ja clas)