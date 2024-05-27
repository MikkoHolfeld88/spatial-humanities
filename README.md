# spatial-humanities
Students Project for spatial humanities in data science studies

## Projektrahmen
#### Vortrag Ende Juni
#### schriftliche Ausarbeitung (bis Ende des Semesters)
#### Anwendung oder Karte

## Projektidee
Visualisierung des patientenzuflusses in medizinische Einrichtungen in Deutschland.

## Anwendung/Karte:
1. Visualisierung einer Deutschalndkarte mit Bevölkerungsverteilung (vermutlich auf Gemeindeebene)
2. Visualisierung von Krankenhäuser und ggf. Arztpraxen in Deutschland als Punkte (Metadaten zu Einrichtungen erfassen)
3. Darstellungen des potentiellen Patientenzuflusses aus den Gemeinden in die Krankenhäsuer (Mappen der Bevölkerungsanzahlen auf die Kapazitäten z.B: vorhandenen betten der Einrichtungen)
4. Interaktives Verändern der medizinischen Einrichtungen:
   - einzelne Krankenhäuser "abschalten"
   - Kapazitäten (z.B. Betten) von Einrichtungen ändern
   - Pandemie Simulation (hohes Aufkommen von Erkrankten)
     --> Darstellen wie sich Flusss von Menschen verändert
## Mehrwert:
Auswirkung von Krankenhausschließungen oder Erweiterungen auf die Versorgungslage unter gegebenen Einschränkungen simulieren

## Projektbericht/Ausarbeitung:
### Ausgangslage/Literatur: 
Anhand von Berichten (muss nicht rein wissenschaftlich sein, Meinung von Ärzten zu Thema kann auch eingebracht werden) eine Liste von ca. 10 Faktoren über Kliniken zusammentragen, welche einen Klinigausbau oder Abbau sowie die Versorgungslage betreffen können. Anhand dessen soll quantifiziert werden, was unsere Anwendung simulieren kann und was nicht.
### Beschreibung von Daten, Vorgehensweise, Anwendung etc.


## Alternative Ideen:
- Visualisierung Wege/Entfernungen und Transportmöglichkeiten zu medizinischen Einrichtungen
- Krankheiten- oder diagnosenspezifische Auswertungen

#Local Installation

### Step ny Step Guid
* Zuerst müssen Sie das Repository klonen
* Anschließend die requirements.txt Datei installieren mit pip install -r requirements.txt
* Dann über das Terminal in den ordner `frontend` wechseln 
* Die Streamlit app kann hier mit dem Befehl `streamlit run app.py` gestartet werden