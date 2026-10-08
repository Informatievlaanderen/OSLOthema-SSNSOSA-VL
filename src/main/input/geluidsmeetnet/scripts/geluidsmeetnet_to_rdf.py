#!/usr/bin/env python3
"""Zet de Aerovision-export (Brussels Airport, EBBR) om naar SSN/SOSA 2023-Turtle.

Invoer  : brondata/<datum>_EBBR_NoiseEvents.csv
          brondata/<datum>_EBBR_NoiseIndicators_Aeronautic_ByDay.csv
          brondata/<datum>_EBBR_Flights.csv
Uitvoer : geluidsmeetnet.trig  — alle meetcampagnes (uitgesloten van de mvn-pipeline)
          geluidsmeetnet.ttl   — validatie-subset: enkel VALIDATIE_CAMPAGNE

Gebruik : python3 scripts/geluidsmeetnet_to_rdf.py   (vanuit src/main/input/geluidsmeetnet/)
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATUM = "20260929"
VALIDATIE_CAMPAGNE = "M072-2"

BASIS = Path(__file__).resolve().parent.parent
BRON = BASIS / "brondata"
LOKAAL = timezone(timedelta(hours=2))  # CEST, zoals in de export (+02:00)

# Aerovision-dag: 07:00 lokale tijd → 07:00 de volgende dag (zie NoiseIndicators: Start/End)
DAG_BEGIN = datetime(2026, 9, 29, 7, 0, tzinfo=LOKAAL)
PERIODES = {  # periode → (begin, einde) — halfopen interval, conform R12
    "dag": (DAG_BEGIN, DAG_BEGIN + timedelta(hours=24)),
    "D": (DAG_BEGIN, DAG_BEGIN + timedelta(hours=12)),
    "E": (DAG_BEGIN + timedelta(hours=12), DAG_BEGIN + timedelta(hours=16)),
    "N": (DAG_BEGIN + timedelta(hours=16), DAG_BEGIN + timedelta(hours=24)),
}
PERIODE_LABEL = {"dag": "etmaal 07:00–07:00", "D": "dagperiode 07:00–19:00",
                 "E": "avondperiode 19:00–23:00", "N": "nachtperiode 23:00–07:00"}

# Dagindicator → (property, periode, procedure, invoer-eigenschappen van de events)
INDICATOREN = {
    "L24":   ("L24",  "dag", "energetische-sommatie", ["SEL"]),
    "Ld":    ("Ld",   "D",   "energetische-sommatie", ["SEL"]),
    "Le":    ("Le",   "E",   "energetische-sommatie", ["SEL"]),
    "Ln":    ("Ln",   "N",   "energetische-sommatie", ["SEL"]),
    "SEL":   ("SEL",  "dag", "energetische-sommatie", ["SEL"]),
    "LAmax": ("LAmax", "dag", "maximum", ["LAmax"]),
    "LAeq":  ("LAeq-vliegtuiggeluid", "dag", "energetisch-gemiddelde-eventduur", ["SEL", "duur"]),
    "Lden":  ("Lden", "dag", "lden", None),  # afgeleid uit Ld, Le, Ln (afgeleide van afgeleiden)
}

EVENT_PROPS = [  # (sleutel, kolom, eenheid)
    ("LAeq", "LAeq (dB)", "unit:DeciB_A"),
    ("LAmax", "LAmax (dB)", "unit:DeciB_A"),
    ("SEL", "SEL", "unit:DeciB_A"),
    ("duur", "Duration (s)", "unit:SEC"),
]

PREFIXEN = """@prefix sosa:    <http://www.w3.org/ns/sosa/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix time:    <http://www.w3.org/2006/time#> .
@prefix qudt:    <http://qudt.org/schema/qudt/> .
@prefix unit:    <http://qudt.org/vocab/unit/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix ex:      <https://example.org/geluidsmeetnet/> .
"""


# --------------------------------------------------------------------------- hulpfuncties

def lees(naam):
    with open(BRON / f"{DATUM}_EBBR_{naam}.csv", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def tijd(s):
    """Aerovision-tijdstempel → aware datetime. Zonder offset = UTC (kolommen First/Last plot)."""
    s = s.strip()
    if s.endswith("+02:00"):
        return datetime.strptime(s, "%m/%d/%Y %I:%M:%S %p %z")
    return datetime.strptime(s, "%m/%d/%Y %I:%M:%S %p").replace(tzinfo=timezone.utc)


def stamp(dt):
    return f'"{dt.astimezone(LOKAAL).isoformat()}"^^xsd:dateTimeStamp'


def sleutel(dt):
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def lokaal(s):
    return tijd(s).astimezone(LOKAAL).strftime("%Y-%m-%d %H:%M:%S")


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def meetpost(campagne):
    return campagne.rsplit("-", 1)[0]


class Uitvoer:
    def __init__(self):
        self.blokken = []
        self.instants = set()

    def blok(self, tekst):
        self.blokken.append(tekst.rstrip() + "\n")

    def instant(self, dt):
        iri = f"ex:instant-{sleutel(dt)}"
        if iri not in self.instants:
            self.instants.add(iri)
            self.blok(f"{iri} a time:Instant ;\n    time:inXSDDateTimeStamp {stamp(dt)} .")
        return iri

    def interval(self, iri, begin, einde, label=None):
        b, e = self.instant(begin), self.instant(einde)
        lab = f"\n    rdfs:label {lit(label)}@nl ;" if label else ""
        self.blok(f"{iri} a time:Interval ;{lab}\n    time:hasBeginning {b} ;\n    time:hasEnd {e} .")
        return iri

    def tekst(self):
        return "\n".join(self.blokken)


# --------------------------------------------------------------------------- statische delen

def statisch(campagnes):
    meetposten = sorted({meetpost(c) for c in campagnes})
    u = []
    u.append("""###############################################################################
### INFRASTRUCTUUR
###############################################################################

ex:omgeving-EBBR a sosa:FeatureOfInterest ;
    rdfs:label "Omgeving van Brussels Airport (EBBR)"@nl ;
    rdfs:comment "Het gebied rond de luchthaven waarin vliegtuiggeluid wordt opgevolgd. De meetposten zijn ruimtelijke monsters van dit gebied."@nl ;
    sosa:hasSample """ + " , ".join(f"ex:meetpost-{m}" for m in meetposten) + """ ;
    sosa:isFeatureOfInterestOf """ + " , ".join(f"ex:sampling-meetpost-{m}" for m in meetposten) + """ .

ex:geluidsmeetnet-EBBR a sosa:System ;
    rdfs:label "Geluidsmeetnet Brussels Airport"@nl ;
    rdfs:comment "Het meetnet als geheel: de geluidsmeters op de meetposten en de Aerovision-rekenmodule die events aan vluchten koppelt en dagindicatoren berekent."@nl ;
    sosa:hasSubSystem ex:aerovision-rekenmodule ,
        """ + " ,\n        ".join(f"ex:geluidsmeter-{c}" for c in campagnes) + """ .

ex:aerovision-rekenmodule a sosa:Sensor , sosa:System ;
    rdfs:label "Aerovision-rekenmodule"@nl ;
    rdfs:comment "Software die de geluidsevents correleert met radarsporen (Flights) en per meetpost en dag de geluidsindicatoren berekent. Een softwareagent die observaties maakt is een sosa:Sensor (R1)."@nl ;
    sosa:isSubSystemOf ex:geluidsmeetnet-EBBR ;
    sosa:implements ex:procedure-energetische-sommatie , ex:procedure-maximum ,
        ex:procedure-energetisch-gemiddelde-eventduur , ex:procedure-lden .
""")
    for m in meetposten:
        cs = [c for c in campagnes if meetpost(c) == m]
        u.append(f"""ex:meetpost-{m} a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample , sosa:Sample ;
    rdfs:label "Meetpost {m}"@nl ;
    rdfs:comment "Geluidsmeetpost {m} van het meetnet rond Brussels Airport. Locatie niet in de Aerovision-export opgenomen."@nl ;
    sosa:isSampleOf ex:omgeving-EBBR ;
    sosa:isResultOf ex:sampling-meetpost-{m} ;
    sosa:isFeatureOfInterestOf {" , ".join(f"ex:collectie-{c}-{DATUM}" for c in cs)} ;
    sosa:hosts {" , ".join(f"ex:geluidsmeter-{c}" for c in cs)} ;
    sosa:inDeployment {" , ".join(f"ex:campagne-{c}" for c in cs)} ;
    sosa:hasProperty ex:prop-LAeq , ex:prop-LAmax , ex:prop-SEL , ex:prop-duur ,
        ex:prop-L24 , ex:prop-Ld , ex:prop-Le , ex:prop-Ln , ex:prop-Lden , ex:prop-LAeq-vliegtuiggeluid .

# Ruimtelijke bemonstering: de keuze van meetpost {m} in de omgeving van de luchthaven (R8, R11).
ex:sampling-meetpost-{m} a sosa:Sampling , sosa:Execution ;
    rdfs:label "Keuze van meetpost {m} in de omgeving van Brussels Airport"@nl ;
    sosa:hasFeatureOfInterest ex:omgeving-EBBR ;
    sosa:hasResult ex:meetpost-{m} .
""")
    for c in campagnes:
        m = meetpost(c)
        u.append(f"""ex:campagne-{c} a sosa:Deployment ;
    rdfs:label "Meetcampagne {c}"@nl ;
    rdfs:comment "Inzet van geluidsmeter {c} op meetpost {m} (kolom 'Campaigns' in de export)."@nl ;
    sosa:deployedSystem ex:geluidsmeter-{c} ;
    sosa:hasUltimateFeatureOfInterest ex:omgeving-EBBR .

ex:geluidsmeter-{c} a sosa:Sensor , sosa:System ;
    rdfs:label "Geluidsmeter campagne {c}"@nl ;
    sosa:isHostedBy ex:meetpost-{m} ;
    sosa:isSubSystemOf ex:geluidsmeetnet-EBBR ;
    sosa:hasDeployment ex:campagne-{c} ;
    sosa:implements ex:procedure-eventmeting ;
    sosa:observes ex:prop-LAeq , ex:prop-LAmax , ex:prop-SEL , ex:prop-duur .
""")

    u.append("""###############################################################################
### PROCEDURE & OBSERVEERBARE EIGENSCHAPPEN
###############################################################################

ex:procedure-eventmeting a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Detectie en meting van een geluidsevent"@nl ;
    rdfs:comment "De geluidsmeter detecteert een geluidsevent (overschrijding van een drempel gedurende een minimale duur) en bepaalt LAeq, LAmax, SEL en duur over het event."@nl ;
    sosa:hasOutput ex:prop-LAeq , ex:prop-LAmax , ex:prop-SEL , ex:prop-duur .

ex:procedure-energetische-sommatie a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Energetische sommatie van SEL over een referentieperiode"@nl ;
    rdfs:comment "L = 10·log10( Σ 10^(SEL_i/10) / T ), met T de duur van de referentieperiode in seconden (86400 voor L24, 43200 voor Ld, 14400 voor Le, 28800 voor Ln). Voor de dag-SEL wordt T = 1 s genomen."@nl ;
    sosa:hasInput ex:prop-SEL ;
    sosa:hasOutput ex:prop-L24 , ex:prop-Ld , ex:prop-Le , ex:prop-Ln , ex:prop-SEL .

ex:procedure-maximum a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Maximum van de event-LAmax over de dag"@nl ;
    sosa:hasInput ex:prop-LAmax ;
    sosa:hasOutput ex:prop-LAmax .

ex:procedure-energetisch-gemiddelde-eventduur a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Energetisch gemiddelde over de cumulatieve eventduur"@nl ;
    rdfs:comment "LAeq = 10·log10( Σ 10^(SEL_i/10) / Σ duur_i ): het gemiddelde niveau tijdens de momenten met vliegtuiggeluid."@nl ;
    sosa:hasInput ex:prop-SEL , ex:prop-duur ;
    sosa:hasOutput ex:prop-LAeq-vliegtuiggeluid .

ex:procedure-lden a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Berekening Lden"@nl ;
    rdfs:comment "Lden = 10·log10( (12·10^(Ld/10) + 4·10^((Le+5)/10) + 8·10^((Ln+10)/10)) / 24 ), Richtlijn 2002/49/EG bijlage I."@nl ;
    sosa:hasInput ex:prop-Ld , ex:prop-Le , ex:prop-Ln ;
    sosa:hasOutput ex:prop-Lden .

ex:prop-LAeq a sosa:Property ;
    rdfs:label "LAeq,T van een geluidsevent"@nl ;
    skos:notation "LAeq,T" ;
    skos:definition "Equivalent continu A-gewogen geluidsdrukniveau over de duur T van het event: het constante niveau dat over T dezelfde totale geluidsenergie heeft als het werkelijke, fluctuerende geluid. T is de duur van het event (ex:prop-duur)."@nl ;
    skos:scopeNote "LAeq,T = 10·log10[ (1/T)·∫ pA²(t) dt / p0² ] dB, met pA(t) de A-gewogen geluidsdruk en p0 = 20 µPa. A-weging is een frequentieweging die de gevoeligheid van het menselijk oor benadert (IEC 61672-1). LAeq is een lineair gemiddelde van de energie; er is geen exponentiële tijdweging (Fast/Slow) bij betrokken. Een verschil van 3 dB is een verdubbeling of halvering van de geluidsenergie."@nl ,
        "De meter registreert het volledige geluid op de meetpost tijdens het event, inclusief achtergrondgeluid; Aerovision schrijft het event daarna toe aan een vlucht. In deze export geldt voor elk van de 1 818 events exact LAE = LAeq,T + 10·log10(T / 1 s): LAeq, SEL en duur zijn dus niet onafhankelijk."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/leq.htm> .

ex:prop-LAmax a sosa:Property ;
    rdfs:label "LAmax"@nl ;
    skos:notation "LAmax" ;
    skos:definition "Het hoogste A-gewogen, tijdgewogen geluidsdrukniveau binnen de phenomenonTime: binnen het event, of op dagniveau het hoogste van alle events."@nl ;
    skos:scopeNote "Een maximum veronderstelt een exponentiële tijdweging: Fast (F, tijdconstante 125 ms; LAFmax) of Slow (S, 1 s; LASmax). Lmax wordt meestal met Fast gemeten; welke weging Aerovision gebruikt, staat niet in de export. LAmax is geen piekniveau (Lpeak): dat is de hoogste momentane geluidsdruk zonder tijdweging. Op dagniveau is LAmax het maximum van de event-LAmax (procedure ex:procedure-maximum)."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/time-weighting.htm> ,
        <https://www.acoustic-glossary.co.uk/definitions-l.htm> .

ex:prop-SEL a sosa:Property ;
    rdfs:label "SEL (LAE)"@nl ;
    skos:notation "LAE" ;
    skos:definition "Sound Exposure Level (geluidsblootstellingsniveau): het constante A-gewogen niveau dat in één seconde dezelfde geluidsenergie bevat als het volledige event, of als alle events samen binnen de phenomenonTime."@nl ;
    skos:scopeNote "LAE = 10·log10[ ∫ pA²(t) dt / (p0²·T0) ] dB, met p0 = 20 µPa en T0 = 1 s. Verband met LAeq: LAE = LAeq,T + 10·log10(T / T0). Anders dan LAeq is SEL geen gemiddelde maar een maat voor de totale energie: een event dat even luid maar twee keer zo lang is, heeft een SEL die 3 dB hoger ligt. Daardoor zijn SEL-waarden energetisch op te tellen: LAE,totaal = 10·log10 Σ 10^(LAE,i/10). Zo worden de dagindicatoren uit de events berekend."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/sound-exposure.htm#sound-exposure-level> .

ex:prop-duur a sosa:Property ;
    rdfs:label "Duur van een geluidsevent"@nl ;
    skos:notation "T" ;
    skos:definition "De tijdsduur van het geluidsevent, van begin tot einde (kolommen Start en End van de export), in seconden. Het is de integratietijd T van LAeq,T."@nl ;
    skos:scopeNote "Begin en einde volgen uit de detectiecriteria van Aerovision (drempelniveau, minimale duur), die niet in de export staan. Een langere duur betekent niet automatisch meer hinder: de energie zit in SEL (LAE = LAeq,T + 10·log10 T)."@nl .

ex:prop-L24 a sosa:Property ;
    rdfs:label "L24"@nl ;
    skos:notation "LAeq,24h" ;
    skos:definition "Equivalent continu A-gewogen geluidsniveau van vliegtuiggeluid over het volledige Aerovision-etmaal (07:00–07:00, T = 86 400 s)."@nl ;
    skos:scopeNote "L24 = 10·log10( Σ 10^(LAE,i/10) / 86 400 ), over de SEL van alle aan vluchten gekoppelde events. Het is een deelniveau: enkel de energie van vliegtuigevents telt mee, tussen de events wordt stilte verondersteld. Het is dus niet het totale omgevingsgeluid op de meetpost."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/leq.htm> .

ex:prop-Ld a sosa:Property ;
    rdfs:label "Ld (Lday)"@nl ;
    skos:notation "Lday" ;
    skos:definition "Dagindicator: equivalent continu A-gewogen geluidsniveau van vliegtuiggeluid over de dagperiode van 12 uur (07:00–19:00, T = 43 200 s)."@nl ;
    skos:scopeNote "Ld = 10·log10( Σ 10^(LAE,i/10) / 43 200 ), over de events van de dagperiode (Period = D). Benaming en periode volgens Richtlijn 2002/49/EG, bijlage I. Daar is Lday een gemiddelde over alle dagperiodes van een jaar; hier gaat het om één dag en enkel om vliegtuiggeluid."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/definitions-l.htm#lday> ,
        <http://data.europa.eu/eli/dir/2002/49/oj> .

ex:prop-Le a sosa:Property ;
    rdfs:label "Le (Levening)"@nl ;
    skos:notation "Levening" ;
    skos:definition "Avondindicator: equivalent continu A-gewogen geluidsniveau van vliegtuiggeluid over de avondperiode van 4 uur (19:00–23:00, T = 14 400 s)."@nl ;
    skos:scopeNote "Le = 10·log10( Σ 10^(LAE,i/10) / 14 400 ), over de events van de avondperiode (Period = E). Richtlijn 2002/49/EG, bijlage I; daar een jaargemiddelde, hier de waarde van één avond voor vliegtuiggeluid."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/definitions-l.htm> ,
        <http://data.europa.eu/eli/dir/2002/49/oj> .

ex:prop-Ln a sosa:Property ;
    rdfs:label "Ln (Lnight)"@nl ;
    skos:notation "Lnight" ;
    skos:definition "Nachtindicator: equivalent continu A-gewogen geluidsniveau van vliegtuiggeluid over de nachtperiode van 8 uur (23:00–07:00, T = 28 800 s)."@nl ;
    skos:scopeNote "Ln = 10·log10( Σ 10^(LAE,i/10) / 28 800 ), over de events van de nachtperiode (Period = N). Richtlijn 2002/49/EG, bijlage I, waar Lnight de indicator voor slaapverstoring is; daar een jaargemiddelde, hier de waarde van één nacht voor vliegtuiggeluid."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/definitions-l.htm> ,
        <http://data.europa.eu/eli/dir/2002/49/oj> .

ex:prop-Lden a sosa:Property ;
    rdfs:label "Lden"@nl ;
    skos:notation "Lden" ;
    skos:definition "Dag-avond-nachtniveau: equivalent A-gewogen geluidsniveau over het etmaal, waarbij het geluid in de avond met 5 dB en in de nacht met 10 dB verzwaard wordt. Het is de indicator voor algemene hinder."@nl ;
    skos:scopeNote "Lden = 10·log10( (12·10^(Ld/10) + 4·10^((Le+5)/10) + 8·10^((Ln+10)/10)) / 24 ), Richtlijn 2002/49/EG, bijlage I. De toeslagen weerspiegelen de grotere hinder van geluid 's avonds en 's nachts. In de richtlijn is Lden een jaargemiddelde; hier gaat het om één etmaal en enkel om vliegtuiggeluid."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/definitions-l.htm#lden> ,
        <http://data.europa.eu/eli/dir/2002/49/oj> .

ex:prop-LAeq-vliegtuiggeluid a sosa:Property ;
    rdfs:label "LAeq tijdens vliegtuiggeluid"@nl ;
    skos:notation "LAeq (Aerovision)" ;
    skos:definition "Equivalent A-gewogen geluidsniveau gemiddeld over de cumulatieve duur van alle aan vluchten gekoppelde events, niet over het etmaal: het gemiddelde niveau tijdens de momenten waarop er vliegtuiggeluid is."@nl ;
    skos:scopeNote "LAeq = 10·log10( Σ 10^(LAE,i/10) / Σ T_i ). Dit is de Aerovision-indicator met naam LAeq; de cumulatieve duur staat in de kolom Duration van NoiseIndicators (bv. 8 971 s voor F040-2). Niet te verwarren met LAeq,24h (L24): LAeq = L24 + 10·log10(86 400 / Σ T_i)."@nl ;
    rdfs:seeAlso <https://www.acoustic-glossary.co.uk/leq.htm> .
""")
    return "\n".join(u)


# --------------------------------------------------------------------------- dynamische delen

def genereer(campagnes, events, indicatoren, vluchten):
    u = Uitvoer()
    u.blok(PREFIXEN)
    u.blok(statisch(campagnes))

    u.blok("""###############################################################################
### VLUCHTEN (bron van de geluidsevents, uit de radargegevens)
###############################################################################""")
    gezien = set()
    for e in events:
        if e["campagne"] not in campagnes or e["vlucht"] in gezien:
            continue
        gezien.add(e["vlucht"])
        r = vluchten.get(e["vluchtsleutel"], e["rij"])
        richting = r.get("Direction", e["rij"]["Direction"])
        cs = r.get("Callsign", r.get("CallSign", "")) or "(geen callsign)"
        reg = r.get("Registration", r.get("Aircraft registration", ""))
        model = r.get("Model", r.get("Aircraft model", ""))
        modes = e["rij"]["Aircraft (Mode S)"]
        omschr = (f"{richting} {r['From']} → {r['To']}, baan {r['Runway']}"
                  + (f", route {r['Route']}" if r.get("Route") else "")
                  + f"; radarspoor {lokaal(r['First plot'])} – {lokaal(r['Last plot'])} (lokale tijd)")
        if e["vluchtsleutel"] not in vluchten:
            omschr += " (vlucht niet in Flights-export; gegevens uit NoiseEvents)"
        u.blok(f"""{e['vlucht']} a prov:Activity ;
    rdfs:label {lit(cs + ' ' + richting + ' ' + r['From'] + '→' + r['To'])}@nl ;
    dcterms:identifier {lit(cs)} ;
    rdfs:comment {lit(omschr)}@nl ;
    prov:used ex:luchtvaartuig-{modes} .""")
        if f"ex:luchtvaartuig-{modes}" not in gezien:
            gezien.add(f"ex:luchtvaartuig-{modes}")
            u.blok(f"""ex:luchtvaartuig-{modes} a prov:Entity ;
    rdfs:label {lit((reg or modes) + ' (' + model + ')')}@nl ;
    dcterms:identifier {lit(modes)} ;
    rdfs:comment {lit('Mode S-adres ' + modes + (', registratie ' + reg if reg else '') + ', type ' + model)}@nl .""")

    u.blok("""###############################################################################
### TIJDSINTERVALLEN VAN DE DAGINDICATOREN (gedeeld door alle meetposten)
###############################################################################""")
    for p, (b, e) in PERIODES.items():
        u.interval(f"ex:interval-{DATUM}-{p}", b, e, f"29 september 2026, {PERIODE_LABEL[p]}")

    for c in campagnes:
        evs = [e for e in events if e["campagne"] == c]
        coll = f"ex:collectie-{c}-{DATUM}"
        u.blok(f"""###############################################################################
### OBSERVATIES — campagne {c}, 29 september 2026 ({len(evs)} events)
###############################################################################

{coll} a sosa:ObservationCollection , sosa:ExecutionCollection ;
    rdfs:label "Geluidsevents campagne {c} op 29 september 2026"@nl ;
    sosa:madeBySensor ex:geluidsmeter-{c} ;
    sosa:usedProcedure ex:procedure-eventmeting ;
    sosa:hasFeatureOfInterest ex:meetpost-{meetpost(c)} ;
    sosa:phenomenonTime ex:interval-{DATUM}-dag ;
    sosa:hasMember {" ,\n        ".join(e['coll'] for e in evs)} .""")

        u.blok("### --- Geluidsevents")
        for e in evs:
            k, r = e["id"], e["rij"]
            u.blok(f"""ex:geluidsevent-{k} a sosa:Stimulus , prov:Entity ;
    rdfs:label "Geluidsevent {c}, maximum om {lokaal(r['Maximum'])}"@nl ;
    sosa:isDetectedBy ex:geluidsmeter-{c} ;
    prov:wasGeneratedBy {e['vlucht']} .

{e['coll']} a sosa:ObservationCollection , sosa:ExecutionCollection ;
    sosa:wasOriginatedBy ex:geluidsevent-{k} ;
    sosa:madeBySensor ex:geluidsmeter-{c} ;
    sosa:usedProcedure ex:procedure-eventmeting ;
    sosa:hasFeatureOfInterest ex:meetpost-{meetpost(c)} ;
    sosa:phenomenonTime ex:interval-{k} ;
    sosa:isMemberOf {coll} ;
    sosa:hasMember {" , ".join(f"ex:obs-{k}-{p}" for p, _, _ in EVENT_PROPS)} .""")
            u.interval(f"ex:interval-{k}", tijd(r["Start"]), tijd(r["End"]))
            for p, kolom, eenheid in EVENT_PROPS:
                if p == "LAmax":  # tijdstip van het maximum is expliciet gegeven
                    pt = u.instant(tijd(r["Maximum"]))
                else:
                    pt = f"ex:interval-{k}"
                u.blok(f"""ex:obs-{k}-{p} a sosa:Observation , sosa:Execution ;
    sosa:observedProperty ex:prop-{p} ;
    sosa:hasFeatureOfInterest ex:meetpost-{meetpost(c)} ;
    sosa:phenomenonTime {pt} ;
    sosa:hasResult ex:resultaat-{k}-{p} ;
    sosa:isMemberOf {e['coll']} .

ex:resultaat-{k}-{p} a sosa:Result ;
    qudt:numericValue {r[kolom]} ;
    qudt:hasUnit {eenheid} ;
    sosa:isResultOf ex:obs-{k}-{p} .""")

        u.blok("### --- Dagindicatoren (afgeleide observaties, buiten de eventcollectie — R13)")
        ind = indicatoren.get(c, {})
        for naam in ["L24", "Ld", "Le", "Ln", "SEL", "LAmax", "LAeq", "Lden"]:
            if naam not in ind or not ind[naam]["Value"]:
                continue
            prop, periode, proc, invoer = INDICATOREN[naam]
            obs = f"ex:obs-{c}-{DATUM}-{prop}"
            if invoer is None:  # Lden ← Ld, Le, Ln
                bronnen = [n for n in ("Ld", "Le", "Ln") if ind.get(n, {}).get("Value")]
                inv = [f"ex:resultaat-{c}-{DATUM}-{n}" for n in bronnen]
                rel = [f"ex:obs-{c}-{DATUM}-{n}" for n in bronnen]
            else:
                sel = [e for e in evs if periode == "dag" or e["rij"]["Period"] == periode]
                inv = [f"ex:resultaat-{e['id']}-{p}" for e in sel for p in invoer]
                rel = [coll]
            regels = [f"{obs} a sosa:Observation , sosa:Execution ;",
                      f"    rdfs:label \"{naam} campagne {c}, 29 september 2026\"@nl ;",
                      f"    sosa:madeBySensor ex:aerovision-rekenmodule ;",
                      f"    sosa:usedProcedure ex:procedure-{proc} ;",
                      f"    sosa:hasFeatureOfInterest ex:meetpost-{meetpost(c)} ;",
                      f"    sosa:observedProperty ex:prop-{prop} ;",
                      f"    sosa:phenomenonTime ex:interval-{DATUM}-{periode} ;",
                      f"    sosa:relatedObservation {' , '.join(rel)} ;"]
            if inv:
                regels.append("    sosa:hasInputValue " + " ,\n        ".join(inv) + " ;")
            regels.append(f"    sosa:hasResult ex:resultaat-{c}-{DATUM}-{prop} .")
            u.blok("\n".join(regels) + f"""

ex:resultaat-{c}-{DATUM}-{prop} a sosa:Result ;
    qudt:numericValue {ind[naam]['Value']} ;
    qudt:hasUnit unit:DeciB_A ;
    sosa:isResultOf {obs} .""")
    return u.tekst()


def main():
    vluchten = {}
    for r in lees("Flights"):
        vluchten[(r["Mode S"], sleutel(tijd(r["First plot"])))] = r

    events = []
    for r in lees("NoiseEvents"):
        c = r["Campaigns"]
        k = f"{c}-{sleutel(tijd(r['Start']))}"
        vs = (r["Aircraft (Mode S)"], sleutel(tijd(r["First plot"])))
        events.append({"campagne": c, "id": k, "rij": r, "coll": f"ex:eventcollectie-{k}",
                       "vluchtsleutel": vs, "vlucht": f"ex:vlucht-{vs[0]}-{vs[1]}"})
    ids = [e["id"] for e in events]
    if len(ids) != len(set(ids)):
        sys.exit("Event-IRI's niet uniek")

    indicatoren = defaultdict(dict)
    for r in lees("NoiseIndicators_Aeronautic_ByDay"):
        indicatoren[r["Campaigns"]][r["Name"]] = r

    alle = sorted({e["campagne"] for e in events})
    (BASIS / "geluidsmeetnet.trig").write_text(genereer(alle, events, indicatoren, vluchten), encoding="utf-8")
    (BASIS / "geluidsmeetnet.ttl").write_text(
        genereer([VALIDATIE_CAMPAGNE], events, indicatoren, vluchten), encoding="utf-8")
    print(f"{len(events)} events, {len(alle)} campagnes → geluidsmeetnet.trig; "
          f"validatie-subset {VALIDATIE_CAMPAGNE} → geluidsmeetnet.ttl")


if __name__ == "__main__":
    main()
