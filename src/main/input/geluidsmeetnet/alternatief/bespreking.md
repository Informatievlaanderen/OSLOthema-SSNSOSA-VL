# Bespreking — Geluidsmeetnet, alternatief: het geluidsevent als emissie

> **Status: discussievoorstel.** Dit is geen herziening van `../geluidsmeetnet.ttl`, maar een
> tweede lezing van dezelfde brondata om de keuze van het FeatureOfInterest te bespreken. De
> argumenten voor en tegen staan in §6. Een tussenvorm (alternatief B) staat in §6.6.

## 1. Wat stelt dit voorbeeld voor?

Hetzelfde geluidsmeetnet rond Brussels Airport (EBBR, Aerovision-export van 29 september 2026,
`../brondata/`), met één andere keuze: het **geluidsevent** is niet langer een `sosa:Stimulus`
dat metingen *aan de meetpost* start. Het is een **emissie** (`wk:Emissie`, ⊂ `prov:Entity`,
`sosa:FeatureOfInterest`), `prov:wasGeneratedBy` de vlucht, en zelf het FOI van LAeq, LAmax, SEL
en duur. Zo volgt het geluid hetzelfde patroon als de lozing in
`../../waterkwaliteit/` (beslisdocument A14: de emissie is wat de handeling oplevert, de
handeling is de activiteit).

Om het verschil zichtbaar te maken, bevat `geluidsmeetnet_emissie.ttl` niet één meetpost maar
**één vlucht**: vertrek TRA15N (B738, Mode S 4853D3, baan 25R om 06:58), die op vier meetposten
een event gaf.

| Event | Meetpost | Start–einde (lokaal) | LAmax | SEL | Afstand toestel |
|---|---|---|---|---|---|
| `ex:geluidsevent-F041-1-20260929T045911Z` | F041 | 06:59:11–07:00:54 | 65.13 | 78.18 | 2 328 m |
| `ex:geluidsevent-F045-1-20260929T045946Z` | F045 | 06:59:46–07:01:07 | 62.85 | 74.01 | 2 683 m |
| `ex:geluidsevent-M071-1-20260929T050018Z` | M071 | 07:00:18–07:01:59 | 64.13 | 77.91 | 1 839 m |
| `ex:geluidsevent-M072-2-20260929T050100Z` | M072 | 07:01:00–07:02:19 | 62.34 | 74.83 | 2 703 m |

## 2. Kleurlegenda

| Kleur | SOSA-concept | Domeinbetekenis |
|---|---|---|
| Blauw (#60c4e4) | Platform / System / Sensor / FeatureOfInterest (gebied) | Meetposten, geluidsmeters, omgeving van de luchthaven |
| Paars licht (#c6a0f5) | sosa:ObservingProcedure | Eventmeting |
| Oranje (#fe7130) | sosa:Property | LAeq, LAmax, SEL, duur |
| Roze (#e54b89) | Observation / ObservationCollection / prov:Activity | Eventmetingen, de vlucht |
| Geel (#f8b622) | wk:Emissie / prov:Entity / sosa:Result / time:Interval / time:Instant | **De geluidsemissies** (FOI), het luchtvaartuig, meetwaarden, tijden |

De emissie staat in het geel, zoals een `sosa:Sample` of een lozing: het is een entiteit die uit
een activiteit voortkomt, geen infrastructuur.

## 3. Infrastructuur (blauwe nodes)

Ongewijzigd ten opzichte van het hoofdmodel (`../bespreking.md` §3), met één verschuiving:

**`ex:meetpost-<id>` — `sosa:Platform`, `sosa:SpatialSample` (+ `sosa:Sample`)**
De meetpost draagt de meter en blijft een ruimtelijk monster van `ex:omgeving-EBBR`. Hij is in
dit alternatief **niet langer het FOI van de eventmetingen**. De eventcollectie verwijst ernaar
met `prov:atLocation`, zoals de waterkwaliteitsobservaties naar de meetput
(`afvalwater_debieten.ttl`). De meetpost blijft wel het FOI van de **dagindicatoren** (§6.4). Die
staan niet in dit bestand, dus de expliciete typering `sosa:FeatureOfInterest` valt hier weg
(de SHACL-shape vraagt dan minstens één `sosa:isFeatureOfInterestOf`). In een volledig model
komt ze terug. Zoals in het hoofdmodel is de meetpost het resultaat van een ruimtelijke
bemonstering (`ex:sampling-meetpost-<id>`, `sosa:Sampling`) van `ex:omgeving-EBBR`.

Geluidsmeters (`sosa:Sensor`), campagnes (`sosa:Deployment`) en het meetnet (`sosa:System`)
zijn ongewijzigd.

## 4. Observatie/Actuatie-structuur (roze nodes)

Per event één `sosa:ObservationCollection` (`alt:eventcollectie-…`). Gedeelde metadata op
collectieniveau: `hasFeatureOfInterest` (**de emissie**), `prov:atLocation` (de meetpost),
`madeBySensor`, `usedProcedure`, `phenomenonTime`. Er is geen dagcollectie: het bestand bevat
per meetpost maar één event.

Voor het event op M072:

| IRI | observedProperty | usedProcedure | hasResult | hasFeatureOfInterest |
|---|---|---|---|---|
| `alt:obs-M072-2-20260929T050100Z-LAeq` | `ex:prop-LAeq` | (collectie) `ex:procedure-eventmeting` | 55.85 dB(A) | `ex:geluidsevent-M072-2-20260929T050100Z` |
| `alt:obs-M072-2-20260929T050100Z-LAmax` | `ex:prop-LAmax` | (collectie) | 62.34 dB(A) | idem |
| `alt:obs-M072-2-20260929T050100Z-SEL` | `ex:prop-SEL` | (collectie) | 74.83 dB(A) | idem |
| `alt:obs-M072-2-20260929T050100Z-duur` | `ex:prop-duur` | (collectie) | 79 s | idem |

`sosa:wasOriginatedBy` en het type `sosa:Stimulus` vallen weg. Ze zouden naar hetzelfde
knooppunt wijzen als `hasFeatureOfInterest`; het verschil tussen "wat de meting start" en "wat
bestudeerd wordt" verdwijnt in deze lezing. SOSA verbiedt de dubbele rol niet: wie de detectie
expliciet wil houden, kan het type `sosa:Stimulus` naast `wk:Emissie` laten staan.

## 5. Procedure en ObservableProperty

Ongewijzigd: `ex:procedure-eventmeting` (geïmplementeerd door elke geluidsmeter) met output
`ex:prop-LAeq`, `ex:prop-LAmax`, `ex:prop-SEL`, `ex:prop-duur`. Wat verandert, is **waarvan** die
eigenschappen zijn: van een emissie in plaats van een plek. Voor `ex:prop-duur` en `ex:prop-SEL`
is dat natuurlijker: een meetpost heeft geen duur, een geluidsevent wel (§6.2).

De definities (symbool, formule, bron) zijn dezelfde als in het hoofdmodel; zie
`../bespreking.md` §5. Kort:

| Property | Symbool | Betekenis |
|---|---|---|
| `ex:prop-LAeq` | LAeq,T | Constant A-gewogen niveau met dezelfde energie als het event, gemiddeld over de eventduur T |
| `ex:prop-LAmax` | LAmax (LAFmax of LASmax) | Hoogste tijdgewogen (Fast/Slow) A-gewogen niveau binnen het event; geen piekniveau |
| `ex:prop-SEL` | LAE | Niveau dat in 1 s dezelfde energie bevat als het hele event: LAE = LAeq,T + 10·log10(T/1 s) |
| `ex:prop-duur` | T | Duur van het event (Start → End), de integratietijd van LAeq,T |

LAeq, SEL en duur beschrijven samen de **energie** van het event (SEL) en hoe die over de tijd
verdeeld is (LAeq, T). Dat zijn eigenschappen van een voorval, wat argument 2 in §6.2
ondersteunt. Ze hangen wel af van de plaats van de meter, wat argument 6.3.1 (immissie)
ondersteunt: dezelfde vlucht geeft op vier meetposten een SEL van 74,0 tot 78,2 dB.

In de lijn van waterkwaliteit (A14.8) zouden dit CSOR-parameteraspecten moeten worden
(bv. *SEL van geluid*). CSOR heeft daar vandaag geen geluidsgrootheden voor.

## 6. Modelleer-keuzes toegelicht

### 6.1 Waarom het geluidsevent als `wk:Emissie` en FOI?

> **Verworpen alternatief:** het hoofdmodel: event als `sosa:Stimulus`, FOI = meetpost.
> **Gekozen aanpak:** `ex:geluidsevent-…` a `wk:Emissie`, `prov:Entity`,
> `sosa:FeatureOfInterest`; `prov:wasGeneratedBy` de vlucht (`prov:Activity`).
> **Motivatie:** de definitie van `wk:Emissie` (A14.8) is ruim: "wat door een bron of activiteit
> in de omgeving (lucht, water of bodem) terechtkomt, beschouwd als entiteit: het resultaat van
> het uitstoten, lozen, weglekken of verspreiden, niet die handeling zelf". A14.8 liet de vraag
> "enkel stoffen of ook warmte, geluid, trillingen (IED)?" bewust open, als vraag over welke
> parameteraspecten op een emissie geobserveerd worden. Dit voorbeeld vult die vraag concreet in.
> Het PROV-patroon is hetzelfde als bij een lozing: activiteit (vlucht ↔ lozen) genereert entiteit
> (geluid ↔ lozing), en de observaties gaan over de entiteit.

### 6.2 Argumenten vóór

1. **Eén emissiepatroon voor water, lucht en geluid.** Een afnemer die emissies bevraagt, vindt
   lozingen en geluid met dezelfde query (`?foi a wk:Emissie ; prov:wasGeneratedBy ?activiteit`).
2. **De eigenschappen passen beter bij het FOI.** SEL, duur en LAeq-over-het-event zijn
   eigenschappen van een *voorval*, niet van een plek. In het hoofdmodel heeft de meetpost een
   "duur van een geluidsevent", wat alleen klopt via de omweg van de stimulus.
3. **Bronattributie wordt het hoofdpad.** Geluidsbeleid rond luchthavens is grotendeels
   brongericht (quotacount per toesteltype, routes, nachtvluchten). Met de vlucht één
   `prov:wasGeneratedBy` van het FOI verwijderd:

   ```sparql
   # Gemiddelde SEL per luchtvaartuig, over alle meetposten
   SELECT ?toestel ?label (AVG(?sel) AS ?gemSEL) WHERE {
     ?obs sosa:observedProperty ex:prop-SEL ;
          sosa:hasFeatureOfInterest/prov:wasGeneratedBy/prov:used ?toestel ;
          sosa:hasResult/qudt:numericValue ?sel .
     ?toestel rdfs:label ?label .            # "PHHXJ (B738)"
   } GROUP BY ?toestel ?label
   ```

   In het hoofdmodel kan dat ook, maar via de collectie: `sosa:isMemberOf/sosa:wasOriginatedBy/prov:wasGeneratedBy`.
4. **Waarom niet de vlucht zelf als FOI?** Dat was in het hoofdmodel verworpen omdat bron en
   effect dan samenvallen. Dit alternatief houdt ze uit elkaar: de vlucht is de activiteit, het
   geluid is de entiteit.

### 6.3 Argumenten tegen

1. **Emissie of immissie?** Een lozing wordt *aan de bron* bemonsterd: de meetput zit op het
   lozingspunt. Een geluidsmeter staat bij de *ontvanger*, 1,8 tot 2,7 km van het toestel. Wat
   hij meet, hangt af van afstand, wind, terrein en reflecties: het is een **immissie**. Een
   emissiegrootheid zou bv. het bronvermogen (LW) van het toestel zijn. De definitie van
   `wk:Emissie` ("wat … in de omgeving terechtkomt") laat beide lezingen toe, maar de RIE-IEPR-
   en VMM-praktijk gaat over de bron.
2. **Eén vlucht, vier emissies.** TRA15N levert vier `wk:Emissie`-instanties met verschillende
   SEL (74.0–78.2 dB). Bij waterkwaliteit is de lozing net **tijdsloos en duurzaam** (A5): 1 619
   lozingen verzamelen jaren aan metingen. Hier bestaat elke emissie 80–100 s, op één plek, en
   heeft ze precies één eventcollectie. Het FOI wordt een kopie van de collectie: per dag 1 818
   extra resources zonder extra informatie.
3. **De restricties van `wk:Emissie` (A14.7) passen niet.** `sosa:isResultOf some sosa:Actuation`
   zegt dat elke emissie het resultaat is van een actuatie. Een vlucht is geen actuatie om geluid
   te maken: geluid is een bijproduct. Dit voorbeeld maakt open punt **A14.9** concreet en
   ondersteunt het voorstel daar (`owl:allValuesFrom`, of enkel `prov:wasGeneratedBy some
   prov:Activity` behouden). Het bestand zet geen `sosa:isResultOf`; met de restricties op
   `owl:minCardinality 0` geeft dat geen SHACL-fout, maar de OWL-betekenis klopt niet.
4. **Twee soorten FOI in één dataset.** De dagindicatoren (L24, Ld, Le, Ln, Lden) zijn volgens
   Richtlijn 2002/49/EG **beoordelingsgrootheden van een plaats** (blootstelling van woningen).
   Hun FOI moet de meetpost blijven (§6.4). De afleiding loopt dan van observaties op emissies naar
   een observatie op een plek. Dat mag in SOSA, maar het hoofdmodel heeft één FOI voor alles.
5. **Namespace.** `wk:` is het waterkwaliteitsvocabularium. Wordt geluid een emissie, dan hoort
   `Emissie` in een generiek omgevingsvocabularium (of RIE-IEPR), niet onder waterkwaliteit.

### 6.4 Waarom blijft de meetpost het FOI van de dagindicatoren?

> **Verworpen alternatief:** een **groep van emissies** als FOI (zoals de groep van lozingen bij
> de vrachten, waterkwaliteit A8): "alle vliegtuiggeluid op M072 op 29 september".
> **Gekozen aanpak:** het FOI van L24…Lden blijft `ex:meetpost-M072` (niet in dit bestand
> uitgewerkt; zie `../geluidsmeetnet.ttl`), met `sosa:hasInputValue` naar de SEL-resultaten van
> de emissies.
> **Motivatie:** Lden is wettelijk gedefinieerd als blootstelling op een plaats. Een "groep van
> emissies op M072" is in feite de meetpost met een tijdsvenster, en het tijdsvenster staat al in
> `sosa:phenomenonTime` (A5).

### 6.5 Waarom `prov:atLocation` op emissie en collectie?

> **Verworpen alternatief:** de meetpost als `sosa:hasUltimateFeatureOfInterest`, of geen
> koppeling (enkel via de sensor en `sosa:isHostedBy`).
> **Gekozen aanpak:** `prov:atLocation ex:meetpost-<id>` op de eventcollectie (zoals op de
> waterkwaliteitsobservaties) én op de emissie.
> **Motivatie:** de meetpost is geen ultiem FOI van de emissie (de emissie is geen monster van
> de meetpost). Maar de emissie bestaat in deze lezing alleen *op* die meetpost: zonder plaats is
> "SEL 74.83" betekenisloos. Dat `prov:atLocation` op de emissie nodig is, is zelf een aanwijzing
> voor argument 6.3.1: het is een effect op een plaats.

### 6.6 Tussenvorm: alternatief B — één emissie per vlucht, het event als monster

Wie het emissiepatroon wil, maar argumenten 6.3.1 en 6.3.2 ernstig neemt, kan het
waterkwaliteitspatroon voor **stalen** volgen (A4: staal als FOI, lozing als ultiem FOI):

```turtle
ex:geluid-vlucht-4853D3-20260929T045809Z a wk:Emissie , prov:Entity , sosa:FeatureOfInterest ;
    prov:wasGeneratedBy ex:vlucht-4853D3-20260929T045809Z .        # één emissie per vlucht, aan de bron

ex:geluidsevent-M072-2-20260929T050100Z a sosa:Sample , sosa:FeatureOfInterest ;
    sosa:isSampleOf ex:geluid-vlucht-4853D3-20260929T045809Z ;    # het geluid van die vlucht, zoals het M072 bereikte
    prov:atLocation ex:meetpost-M072 .

alt:eventcollectie-M072-2-20260929T050100Z
    sosa:hasFeatureOfInterest ex:geluidsevent-M072-2-20260929T050100Z ;
    sosa:hasUltimateFeatureOfInterest ex:geluid-vlucht-4853D3-20260929T045809Z .
```

Voordelen: één emissie per vlucht (bron), de vier events zijn vier monsters ervan (ontvanger),
emissie en immissie zijn gescheiden, en het patroon is identiek aan staal ↔ lozing. Nadeel: een
"monster" van een geluidsveld is een abstractie (er wordt niets weggenomen), en de event-sample
is niet het resultaat van een expliciete `sosa:Sampling`. Zie `geluidsmeetnet_vergelijking.mmd`.

### 6.7 Discussievragen

1. Is wat een geluidsmeter op 2 km van het toestel registreert een emissie, of een immissie die
   een eigen klasse verdient?
2. Is een emissie per definitie duurzaam (tijdsloos, A5), of mag ze ook een voorval van 80 s
   zijn?
3. Moet `wk:Emissie` (of een generieke opvolger) ook geluid, trillingen en warmte dekken? Zo ja,
   welke CSOR-parameteraspecten zijn nodig?
4. Welke van de drie varianten (hoofdmodel, A, B) maakt de meest gestelde vragen van gebruikers
   (per meetpost, per vlucht, per toesteltype, per nachtperiode) het eenvoudigst?
5. Bevestigt dit voorbeeld dat de restricties `isResultOf some Actuation` en `wasDerivedFrom
   some Procedure` op `wk:Emissie` (A14.9) te streng zijn?

## 7. Tijdsmodellering

Zoals het hoofdmodel: `sosa:phenomenonTime → time:Interval → time:hasBeginning/hasEnd →
time:Instant → time:inXSDDateTimeStamp` voor het event, en een `time:Instant` (het moment van het
maximum) voor LAmax. De emissie zelf krijgt **geen** tijd: de tijd staat op de observaties (A5).
Merk op dat de emissie hier wel de facto een tijdspanne heeft (het interval van haar enige
collectie); dat is argument 6.3.2.

Twee events van TRA15N (F041-1, F045-1) beginnen vóór 07:00 en vallen dus deels in het vorige
Aerovision-etmaal. Dat is de afkapping die in het hoofdmodel de kleine afwijking bij F041-1 en
F045-1 verklaart (`../bespreking.md` §6).

## 8. Prefixen en IRI-structuur

| Prefix | Base URI | Tijdelijk of persistent |
|---|---|---|
| `sosa:` | `http://www.w3.org/ns/sosa/` | Persistent (W3C) |
| `prov:` | `http://www.w3.org/ns/prov#` | Persistent (W3C) |
| `time:` | `http://www.w3.org/2006/time#` | Persistent (W3C) |
| `qudt:` | `http://qudt.org/schema/qudt/` | Persistent (QUDT) |
| `unit:` | `http://qudt.org/vocab/unit/` | Persistent (QUDT) |
| `dcterms:` | `http://purl.org/dc/terms/` | Persistent (DCMI) |
| `wk:` | `https://data.vlaanderen.be/ns/waterkwaliteit#` | Persistent (OSLO), ontwerpversie |
| `xsd:`, `rdfs:` | W3C | Persistent |
| `ex:` | `https://example.org/geluidsmeetnet/` | Tijdelijk; **dezelfde IRI's als het hoofdmodel** |
| `alt:` | `https://example.org/geluidsmeetnet/alternatief/` | Tijdelijk; collecties, observaties en resultaten van dit alternatief |

Vlucht, meetposten, meters, eigenschappen, procedure, tijd en de events zelf hebben dezelfde
`ex:`-IRI als in `../geluidsmeetnet.ttl`. Zo is te zien dat het event dezelfde resource is, met
een andere rol. Collecties, observaties en resultaten staan onder `alt:`, zodat beide modellen in
één store passen zonder dat een observatie twee FOI's krijgt. Geen blank nodes.

## 9. Inverse relaties

| Relatie | Inverse | Opgenomen in | Doel |
|---|---|---|---|
| `prov:wasGeneratedBy` | `prov:generated` | emissie ↔ vlucht | Vanuit een vlucht al haar emissies vinden (hier 4) |
| `sosa:hasFeatureOfInterest` | `sosa:isFeatureOfInterestOf` | eventcollectie ↔ emissie | Vanuit de emissie haar metingen |
| `sosa:hosts` | `sosa:isHostedBy` | meetpost ↔ meter | Ongewijzigd |
| `sosa:hasSubSystem` | `sosa:isSubSystemOf` | meetnet ↔ meters | Ongewijzigd |
| `sosa:deployedSystem` | `sosa:hasDeployment` | campagne ↔ meter | Ongewijzigd |
| `sosa:hasSample` | `sosa:isSampleOf` | omgeving ↔ meetpost | Ongewijzigd |
| `sosa:hasMember` | `sosa:isMemberOf` | eventcollectie ↔ observatie | Ongewijzigd |
| `sosa:hasResult` | `sosa:isResultOf` | observatie ↔ resultaat | Ongewijzigd |

`prov:generated` is nieuw ten opzichte van het hoofdmodel: in dit alternatief is "alle geluid
van vlucht X" de hoofdvraag, en die moet zonder inferentie op te vragen zijn.
