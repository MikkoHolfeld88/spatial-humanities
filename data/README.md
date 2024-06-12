## data

### Daten zu Krankenhäusern
https://www.statistikportal.de/de/veroeffentlichungen/krankenhausverzeichnis

Rohdaten: "Krankenhausverzeichnis_31_12_2022__1.xlsb"<br>
Vorverarbeitete Daten: **hospitals_saxony.geojson**

Nutzung als GeoJson angereichert mit foglenden Attributen:

| Land | Kreis | Gemeinde | Name_Einrichtung | Adresse | Geokoordinate | Traeger | Einrichtungstyp | Allgemeine_Notfallversorgung | Betten insgesamt | Betten innere Medizin | Betten Kardiologie | Betten Allgemeine Chirurgie |Betten Herzchirurgie |Betten Urologie | Betten HNO | Betten Psychatrie |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |------------- |------------- | ------------- | ------------- |
| Number | Number | Number | String | String | Point | Number | Number | Boolean | Number | Number | Number | Number | Number | Number | Number | Number |

### Gemeinden mit metainformation zu Bevölkerung und Fläche:
Gemeinden mit Bevölkerungsinfomration: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV1QAktuell.html<br>

Rohdaten: "Gemeindedaten.xlsx"<br>
Vorverarbeitete Daten: **cities_saxony.geojson**<br>

Nutzung als GeoJson angereichert mit foglenden Attributen:

| Land | RB | Kreis | Gemeinde | Gemeindename | Bevölkerung Insgesamt | Bevölkerung männlich | Bevölkerung weiblich | Bevölkerung je km2 | Geografische Mittelpunktkoordianten | Geometry (Grenze) |
| ---- | -- | ----- | ---------| -------------| --------------------- | -------------------- | -------------------- |------------------- |------------------------------------ |------------------ |
| Number | Number | Number | Number | String | Number | Number | Number | Number | Point (asl wkt) | Polygon | 

### fertige Datensätze:
- "cities_saxony.geojson"
- "hospitals_saxony.geojson"
