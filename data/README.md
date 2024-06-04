## data

### Daten zu Krankenhäusern
https://www.statistikportal.de/de/veroeffentlichungen/krankenhausverzeichnis
"Krankenhausverzeichnis_31_12_2022__1.xlsb"

Nutzung als GeoJson angereichert mit foglenden Attributen:

| Land | Kreis | Gemeinde | Name_Einrichtung | Adresse | Geokoordinate | Traeger | Schwerverletztenversorgung | Schlaganfallversorgung | Betten insgesamt | Betten innere Medizin | Betten Kardiologie | Betten Allgemeine Chirurgie |Betten Herzchirurgie |Betten Urologie | Betten HNO | Betten Psychatrie |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |------------- |------------- | ------------- | ------------- |
| Number | Number | Number | String | String | Coordinate | Number | Boolean | Boolean | Number | Number | Number | Number | Number | Number | Number | Number |

### Gemeinden mit metainformation zu Bevölkerung und Fläche:
Gemeinden mit Bevölkerungsinfomration: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV1QAktuell.html
"Gemeindedaten.xlsx"

Nutzung als GeoJson angereichert mit foglenden Attributen:

| Land | Kreis | Gemeinde | Gemeindename | Bevölkerungsanzahl | Geografische Mittelpunktkoordianten | Grenze als GeoJson|
| ---- | ----- | -------- | ------------ | ------------------ | ----------------------------------- | ----------------- | 
| Number | Number | Number | String | Number | coordinate | GeoJson | 

### fertige Datensätze:
- "cities.geojson"
- "hospitals.geojson"
- "Patientenfluss.csv"
