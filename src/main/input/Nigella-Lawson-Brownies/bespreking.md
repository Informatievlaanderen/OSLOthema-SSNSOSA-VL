1. Wat doet het SDS-artikel precies?

Het werk van Pieter Colpaert en co-auteurs introduceert SDS (Smart Data Specification) als:

een metadata/vocabulairelaag bovenop bestaande standaarden zoals DCAT, PROV-O en P-Plan
met focus op:
data streams (LDES)
transformaties tussen datasets
provenance voor datasetselectie

👉 Belangrijk: SDS modelleert niet het proces zelf, maar:

de data die uit processen komt
de transformaties tussen datasets/streams
en hoe een query agent daar slim mee omgaat
2. Wat doet jouw brownies-voorbeeld?

Jouw model doet bijna het omgekeerde:

Het gebruikt P-Plan + PROV-O + SSN/SOSA
en modelleert:
het volledige proces zelf (plan → deployment → execution)
inclusief:
stappen
resources (machines, ingrediënten)
observaties en actuaties
concrete uitvoering met tijd en causale relaties

👉 Dit is geen datasetbeschrijving, maar een end-to-end proces digital twin in RDF.

3. Overlap (waar Colpaert “oude wijn” zou zien)

Er zijn duidelijke raakpunten:

Je gebruikt exact dezelfde bouwstenen:
PROV-O
P-Plan
Je modelleert ook transformaties en herkomst
Het idee “provenance helpt betere keuzes maken” zit impliciet ook in jouw model

👉 Vanuit dat perspectief:
conceptueel zit je binnen een bestaand paradigma (semantic web + provenance)

Dus ja, als je claim is:

“we modelleren processen met P-Plan/PROV”
dan is het inderdaad niet nieuw.

4. Waar jouw werk wél potentieel nieuw is

Hier zit het interessante deel. Jij doet namelijk iets wat SDS niet doet:

1. Van data-provenance → proces-provenance
   SDS: “waar komt deze dataset vandaan?”
   Jij: “hoe is dit fysiek/industrieel proces uitgevoerd?”

👉 Dat is een andere laag.

2. Integratie van planning + execution + IoT

Je combineert:

P-Plan (abstract plan)
PROV-O (traceerbaarheid)
SSN/SOSA (sensoren & actuatoren)

👉 Die drie-lagen integratie is zelden zo volledig uitgewerkt.

3. Digital twin achtige modellering

Je model:

koppelt abstract recept → concrete uitvoering → fysieke systemen
met tijd, afhankelijkheden en observaties

👉 Dit lijkt op:

Industry 4.0 / Digital Twins
maar dan volledig semantisch en interoperabel
4. Generaliseerbaarheid

Je zegt expliciet:

“staat voor het modelleren van om het even welk industrieel proces”

👉 Als je dat aantoont, heb je een sterke bijdrage:

van brownies → fabriek → logistiek → chemische processen
5. De echte zwakke plek (waar reviewers op schieten)

Als je het nu zou indienen, krijg je waarschijnlijk:

“Nice modeling exercise, but what is the contribution?”

Problemen:

Geen nieuw vocabulaire (je hergebruikt bestaande)
Geen algoritme / systeem
Geen evaluatie (performance, usability, etc.)
Geen duidelijke use case beyond demo

👉 Dat maakt het risico op “oude wijn” reëel.

6. Hoe maak je er wél een publishable bijdrage van?

Hier zijn concrete richtingen die het wél nieuw maken:

A. Brug slaan met SDS (sterk!)
Toon hoe jouw procesmodel:
automatisch SDS-beschrijvingen kan genereren
of dataset-provenance kan verrijken

👉 Dan verbind je:

process layer (jij)
data layer (SDS)

➡️ Dat is wél origineel.

B. Querying / reasoning

Bijvoorbeeld:

“Geef alle producten beïnvloed door een defecte machine”
“Welke stap veroorzaakte kwaliteitsverlies?”

👉 Als je dit oplost:

met SPARQL / reasoning
en aantoont dat het werkt

➡️ dan heb je een echte bijdrage

C. Industrie use case
productieproces
supply chain
IoT pipeline

👉 Brownies = demo
👉 Industrie = paper

D. Complexity / scalability
Hoe schaalbaar is zo’n model?
Wat kost het?
7. Eindoordeel

Kort maar eerlijk:

Zonder extra bijdrage →
✔️ “oude wijn in nieuwe zakken” (mooie demonstrator)
Met juiste framing en uitbreiding →
✔️ sterke paper/poster, vooral als:

je het positioneert als:

“semantic digital twin modeling with integrated provenance”

én linkt met SDS / LDES
8. Mijn advies

Ga niet verdedigen dat het “nieuw” is op vocabulaire-niveau.
Dat is het niet.

Positioneer het als:

“een integratie en operationalisatie van bestaande ontologieën voor end-to-end procesmodellering, met toepassingen in digital twins en data provenance”

Dat is:

eerlijk
verdedigbaar
en publishable

