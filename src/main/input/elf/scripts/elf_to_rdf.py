#!/usr/bin/env python3
"""Zet de ELF-meetgegevens (ThingsBoard-export) en de sensorregistratie (Jira) om naar SSN/SOSA 2023.

Invoer  : source/_meetperiode_SENS-269_ELF_C_0020_<gemeente>.parquet  (gepseudonimiseerd, scripts/anonimiseer.py)
              telemetrie van ELF-node ELF_C_0020 in sleutel-waardevorm (één rij per tijdstip en sleutel)
          source/elf_sensors_registratie.csv  (gepseudonimiseerd)
              Jira-export (project SENS): één ticket per meetcampagne (sensor, adres, start, einde)
Uitvoer : elf.trig  — één volledige lokale dag (VOLLEDIGE_DAG) met uur- en dagindicatoren, alle meetcampagnes
                      (Turtle-inhoud; uitgesloten van de bulkvalidatie)
          elf.ttl   — validatie-subset: één uur (VALIDATIE_UUR) met uurindicatoren, de campagnes in
                      VALIDATIE_CAMPAGNES

Gebruik : python3 scripts/elf_to_rdf.py   (vanuit src/main/input/elf/; vereist pandas en pyarrow)

Lezing (zie bespreking.md §6): blootstelling op een plaats, zoals de geluidsimmissie in geluidsmeetnet/. De
meetlocatie is een ruimtelijk monster van de omgeving van een hoogspanningsverbinding of -station; die bron
is een apart studieobject. De registratie koppelt een sensor nog niet aan een bron: de bronnen hier zijn
fictief, één per (gepseudonimiseerde) gemeente.

Fictieve gegevens, deterministisch afgeleid uit de gepseudonimiseerde waarden (geen echte positie):
  - de geometrie van een meetlocatie (Lambert 72), afgeleid uit het fictieve adres;
  - de bron (verbinding of station, spanningsniveau) per gemeente.

Niet omgezet: de apparaatstatus (lastConnectTime, lastActivityTime, …, active, inactivityTimeout): gegevens
over de verbinding van het apparaat met ThingsBoard, geen waarnemingen van het veld.
"""
import csv
import hashlib
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

BASIS = Path(__file__).resolve().parent.parent
PARQUET = next((BASIS / "source").glob("_meetperiode_SENS-269_ELF_C_0020_*.parquet"))
REGISTRATIE = BASIS / "source" / "elf_sensors_registratie.csv"

LOKAAL = ZoneInfo("Europe/Brussels")
VOLLEDIGE_DAG = date(2025, 11, 27)                        # lokale dag voor elf.trig
VALIDATIE_UUR = datetime(2025, 11, 27, 10, tzinfo=LOKAAL)  # lokaal uur voor elf.ttl
VALIDATIE_CAMPAGNES = ["SENS-269", "SENS-270", "SENS-229"]  # zelfde locatie + eerdere inzet ELF_C_0025
PEILDATUM = date(2026, 11, 3)  # registratie-einden na deze datum zijn gepland, niet voorbij

# Meetwaarden: (sleutel in ThingsBoard, label, definitie)
METINGEN = [
    ("RMStotal", "totale RMS-waarde van de magnetische fluxdichtheid",
     "Effectieve waarde (RMS) van de grootte van de magnetische fluxdichtheidsvector over de drie assen. "
     "In de bron geldt telkens RMStotal = 1,2374 × √(Xpeak_low² + Ypeak_low² + Zpeak_low²)."),
    ("Xpeak_low", "piekwaarde 'low' langs de X-as", "Component langs de X-as van de magnetische fluxdichtheid, kanaal 'low'."),
    ("Ypeak_low", "piekwaarde 'low' langs de Y-as", "Component langs de Y-as van de magnetische fluxdichtheid, kanaal 'low'."),
    ("Zpeak_low", "piekwaarde 'low' langs de Z-as", "Component langs de Z-as van de magnetische fluxdichtheid, kanaal 'low'."),
    ("Xpeak_high", "piekwaarde 'high' langs de X-as", "Component langs de X-as van de magnetische fluxdichtheid, kanaal 'high'."),
    ("Ypeak_high", "piekwaarde 'high' langs de Y-as", "Component langs de Y-as van de magnetische fluxdichtheid, kanaal 'high'."),
    ("Zpeak_high", "piekwaarde 'high' langs de Z-as", "Component langs de Z-as van de magnetische fluxdichtheid, kanaal 'high'."),
]
SLEUTELS = [m[0] for m in METINGEN]

# Indicatoren van RMStotal (business case: actuele waarde, minimum en maximum per periode, gemiddelde
# blootstelling). (statistiek, procedure voor een uur uit minuutwaarden, procedure voor een dag uit uurwaarden)
INDICATOREN = [
    ("minimum", "procedure-minimum", "procedure-minimum"),
    ("maximum", "procedure-maximum", "procedure-maximum"),
    ("gemiddelde", "procedure-uurgemiddelde", "procedure-daggemiddelde"),
]

MEERVOUD = {"minimum": "uurminima", "maximum": "uurmaxima", "gemiddelde": "uurgemiddelden"}

MAANDEN = {"jan": 1, "feb": 2, "mrt": 3, "apr": 4, "mei": 5, "jun": 6,
           "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12}

# Lambert 72: ruwe omhullende van Vlaanderen, voor de fictieve punten
LAMBERT72 = "<http://www.opengis.net/def/crs/EPSG/0/31370>"
X_BEREIK, Y_BEREIK = (25_000, 255_000), (155_000, 240_000)

PREFIXEN = """@prefix sosa:         <http://www.w3.org/ns/sosa/> .
@prefix prov:         <http://www.w3.org/ns/prov#> .
@prefix time:         <http://www.w3.org/2006/time#> .
@prefix qudt:         <http://qudt.org/schema/qudt/> .
@prefix unit:         <http://qudt.org/vocab/unit/> .
@prefix quantitykind: <http://qudt.org/vocab/quantitykind/> .
@prefix geo:          <http://www.opengis.net/ont/geosparql#> .
@prefix dcterms:      <http://purl.org/dc/terms/> .
@prefix xsd:          <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:         <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:         <http://www.w3.org/2004/02/skos/core#> .
@prefix ex:           <https://example.org/elf/> .
"""


def lit(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def slug(s: str) -> str:
    s = s.strip().lower()
    for a, b in (("é", "e"), ("è", "e"), ("ë", "e"), ("ï", "i"), ("ö", "o"), ("ü", "u"), ("–", "-")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def hashgetal(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def ts_utc(t: pd.Timestamp) -> str:
    """xsd:dateTimeStamp in UTC, zoals de bron (milliseconden behouden)."""
    return t.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def ts_id(t: pd.Timestamp) -> str:
    """Deterministisch IRI-fragment uit het tijdstip (UTC, met milliseconden)."""
    return t.tz_convert("UTC").strftime("%Y%m%dT%H%M%S") + f"{t.microsecond // 1000:03d}Z"


def jira_datum(s: str) -> datetime:
    """'26/nov/25 12:00 AM' → middernacht lokale tijd (de registratie bevat enkel datums)."""
    dag, maand, rest = s.strip().split("/", 2)
    jaar = int(rest.split()[0]) + 2000
    return datetime(jaar, MAANDEN[maand.lower()], int(dag), tzinfo=LOKAAL)


def num(v: float) -> str:
    s = f"{v:.5f}".rstrip("0").rstrip(".")
    return s if "." in s else s + ".0"


# ---------------------------------------------------------------------------
# Fictieve bron en geometrie
# ---------------------------------------------------------------------------

def fictieve_bron(gemeente: str) -> dict:
    """Eén fictieve bron per gemeente: een verbinding (380, 150 of 70 kV) of een station."""
    h = hashgetal("bron#" + gemeente)
    kv = (380, 150, 70)[h % 3]
    if (h // 3) % 4 == 0:
        return {"id": f"station-{slug(gemeente)}", "kv": kv,
                "label": f"Hoogspanningsstation {gemeente} ({kv} kV, fictief)", "soort": "hoogspanningsstation"}
    return {"id": f"verbinding-{slug(gemeente)}", "kv": kv,
            "label": f"{kv} kV-verbinding bij {gemeente} (fictief)", "soort": "hoogspanningsverbinding"}


def fictief_punt(locatie: str) -> tuple[int, int]:
    h = hashgetal("punt#" + locatie)
    x = X_BEREIK[0] + h % (X_BEREIK[1] - X_BEREIK[0])
    y = Y_BEREIK[0] + (h // 1_000_003) % (Y_BEREIK[1] - Y_BEREIK[0])
    return x, y


# ---------------------------------------------------------------------------
# Registratie (Jira): sensoren, meetlocaties, meetcampagnes
# ---------------------------------------------------------------------------

def lees_registratie():
    campagnes = []
    with open(REGISTRATIE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            straat = r["Custom field (Straat)"].strip()
            nr = r["Custom field (Huisnummer)"].strip()
            postcode = r["Custom field (Postcode)"].strip()
            gemeente = r["Custom field (Gemeente)"].strip()
            campagnes.append({
                "ticket": r["Issue key"].strip(),
                "sensor": r["Titel"].strip(),
                "start": jira_datum(r["Custom field (Datum start metingen)"]),
                "einde": jira_datum(r["Custom field (Datum einde metingen)"]),
                "adres": f"{straat} {nr}, {postcode} {gemeente}",
                "locatie": f"{postcode}-{slug(straat)}-{slug(nr)}",
                "gemeente": gemeente,
                "bron": fictieve_bron(gemeente),
            })
    return campagnes


def eigenschappen() -> str:
    return " , ".join("ex:prop-" + k for k in SLEUTELS)


def infrastructuur(campagnes) -> str:
    out = []
    sensoren = sorted({c["sensor"] for c in campagnes})
    locaties, bronnen = {}, {}
    for c in campagnes:
        locaties.setdefault(c["locatie"], {"c": c, "tickets": []})["tickets"].append(c["ticket"])
        bronnen.setdefault(c["bron"]["id"], {"bron": c["bron"], "locaties": set()})["locaties"].add(c["locatie"])

    out.append("""###############################################################################
### INFRASTRUCTUUR
###############################################################################
# Sensoren en meetlocaties uit de registratie (Jira, project SENS). Een sensor staat niet vast op
# één locatie (ELF_C_0025 stond eerst in Bloedhoven, daarna in Duisterwijk): de koppeling loopt via de
# meetcampagne (sosa:Deployment), niet via een tijdloze sosa:hosts.
""")
    for s in sensoren:
        mijn = [c for c in campagnes if c["sensor"] == s]
        out.append(f"""ex:sensor-{s} a sosa:Sensor , sosa:System ;
    rdfs:label {lit("ELF-meter " + s)}@nl ;
    dcterms:identifier {lit(s)} ;
    rdfs:comment "ELF-node die het laagfrequente magnetische veld langs drie assen meet en de waarden ongeveer elke minuut naar ThingsBoard stuurt (device_type 'elf-node')."@nl ;
    sosa:implements ex:procedure-elf-meting ;
    sosa:observes {eigenschappen()} ;
    sosa:hasDeployment {" , ".join("ex:meetcampagne-" + c["ticket"] for c in mijn)} .
""")

    out.append("""###############################################################################
### BRONNEN EN HUN OMGEVING
###############################################################################
# De bron van het veld (verbinding of station) en de omgeving waarin ze het veld bepaalt, zoals de
# omgeving van de luchthaven in geluidsmeetnet/. Fictief: de registratie koppelt een sensor nog niet aan
# een bron.
""")
    for bid, b in sorted(bronnen.items()):
        bron = b["bron"]
        out.append(f"""ex:{bid} a sosa:FeatureOfInterest ;
    rdfs:label {lit(bron["label"])}@nl ;
    rdfs:comment {lit(f"{'Fictief' if bron['soort'].endswith('station') else 'Fictieve'} {bron['soort']} ({bron['kv']} kV). In productie een verwijzing naar de verbinding of het station bij de netbeheerder.")}@nl ;
    sosa:hasProperty ex:prop-stroombelasting .

ex:omgeving-{bid} a sosa:FeatureOfInterest ;
    rdfs:label {lit("Omgeving van " + bron["label"])}@nl ;
    rdfs:comment "Het gebied waarin het magnetische veld van de bron de blootstelling bepaalt. De meetlocaties zijn ruimtelijke monsters van dit gebied."@nl ;
    prov:wasInfluencedBy ex:{bid} ;
    sosa:hasSample {" , ".join("ex:meetlocatie-" + l for l in sorted(b["locaties"]))} .
""")

    out.append("""###############################################################################
### MEETLOCATIES
###############################################################################
# Ruimtelijk monster van de omgeving van een bron (R11), met het adres uit de registratie
# (prov:atLocation) en een geometrie (geo:hasGeometry). De geometrie is fictief: afgeleid uit het
# gepseudonimiseerde adres, niet uit een echte positie.
""")
    for loc, d in sorted(locaties.items()):
        c = d["c"]
        x, y = fictief_punt(loc)
        bid = c["bron"]["id"]
        out.append(f"""ex:meetlocatie-{loc} a sosa:Platform , sosa:FeatureOfInterest , sosa:SpatialSample , sosa:Sample ;
    rdfs:label {lit("Meetlocatie " + c["adres"])}@nl ;
    rdfs:comment "De plaats waar de ELF-meter opgesteld staat en waar de blootstelling aan het magnetische veld bestudeerd wordt."@nl ;
    sosa:isSampleOf ex:omgeving-{bid} ;
    sosa:isResultOf ex:sampling-meetlocatie-{loc} ;
    prov:atLocation ex:adres-{loc} ;
    geo:hasGeometry ex:geom-{loc} ;
    sosa:hasProperty {eigenschappen()} ;
    sosa:inDeployment {" , ".join("ex:meetcampagne-" + t for t in d["tickets"])} .

ex:sampling-meetlocatie-{loc} a sosa:Sampling , sosa:Execution ;
    rdfs:label {lit(f"Keuze van meetlocatie {c['adres']} in de omgeving van {c['bron']['label']}")}@nl ;
    sosa:hasFeatureOfInterest ex:omgeving-{bid} ;
    sosa:hasResult ex:meetlocatie-{loc} .

ex:adres-{loc} a prov:Location ;
    rdfs:label {lit(c["adres"])}@nl .

ex:geom-{loc} a geo:Geometry ;
    geo:asWKT {lit(f"{LAMBERT72} POINT({x} {y})")}^^geo:wktLiteral ;
    rdfs:comment "Fictief punt, afgeleid uit het gepseudonimiseerde adres. In productie: de exacte locatie uit de registratie, of de adrespositie uit het Adressenregister."@nl .
""")

    out.append("""ex:conversiescript a sosa:Sensor , sosa:System ;
    rdfs:label "Conversiescript elf_to_rdf.py"@nl ;
    rdfs:comment "Software die de uur- en dagindicatoren berekent uit de minuutwaarden. De indicatoren staan niet in de bron; in productie berekent het dataplatform ze."@nl ;
    sosa:implements ex:procedure-minimum , ex:procedure-maximum , ex:procedure-uurgemiddelde , ex:procedure-daggemiddelde .
""")
    return "\n".join(out)


def campagnes_ttl(campagnes) -> str:
    out = ["""###############################################################################
### MEETCAMPAGNES (sosa:Deployment)
###############################################################################
# Eén Jira-ticket = één meetcampagne. Start en einde uit de registratie (enkel datums, middernacht
# lokale tijd). Een einde na de peildatum is een gepland einde en wordt niet als prov:endedAtTime
# opgenomen. Het uiteindelijke doel van de campagne is de omgeving van de bron.
"""]
    for c in campagnes:
        regels = [f"""ex:meetcampagne-{c["ticket"]} a sosa:Deployment ;
    rdfs:label {lit(f'Meetcampagne {c["ticket"]}: {c["sensor"]} op {c["adres"]}')}@nl ;
    dcterms:identifier {lit(c["ticket"])} ;
    sosa:deployedSystem ex:sensor-{c["sensor"]} ;
    sosa:deployedOnPlatform ex:meetlocatie-{c["locatie"]} ;
    sosa:hasFeatureOfInterest ex:meetlocatie-{c["locatie"]} ;
    sosa:hasUltimateFeatureOfInterest ex:omgeving-{c["bron"]["id"]} ;
    prov:startedAtTime {lit(c["start"].isoformat())}^^xsd:dateTime"""]
        if c["einde"].date() <= PEILDATUM:
            regels.append(f"""    prov:endedAtTime {lit(c["einde"].isoformat())}^^xsd:dateTime""")
        else:
            regels.append(f"""    rdfs:comment {lit("Gepland einde: " + c["einde"].date().isoformat() + ".")}@nl""")
        out.append(" ;\n".join(regels) + " .\n")
    return "\n".join(out)


def procedures() -> str:
    out = ["""###############################################################################
### PROCEDURE EN EIGENSCHAPPEN
###############################################################################

ex:procedure-elf-meting a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Driedimensionale meting van het laagfrequente magnetische veld"@nl ;
    rdfs:comment "De ELF-node meet de magnetische fluxdichtheid langs drie assen en rapporteert ongeveer elke minuut zeven waarden: per as een waarde 'low' en 'high', en een totale RMS-waarde. Meetvenster, frequentieband en betekenis van 'low' en 'high' zijn niet in de bron beschreven."@nl ;
    sosa:hasOutput """ + eigenschappen() + """ .

ex:procedure-minimum a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Minimum van RMStotal over een periode"@nl ;
    rdfs:comment "Kleinste inputwaarde. Voor een uur: de minuutwaarden met resultaattijd in het lokale uur [hh:00, hh+1:00). Voor een dag: de uurminima van die dag."@nl ;
    sosa:hasInput ex:prop-RMStotal ;
    sosa:hasOutput ex:prop-RMStotal .

ex:procedure-maximum a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Maximum van RMStotal over een periode"@nl ;
    rdfs:comment "Grootste inputwaarde. Voor een uur: de minuutwaarden met resultaattijd in het lokale uur [hh:00, hh+1:00). Voor een dag: de uurmaxima van die dag."@nl ;
    sosa:hasInput ex:prop-RMStotal ;
    sosa:hasOutput ex:prop-RMStotal .

ex:procedure-uurgemiddelde a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Uurgemiddelde van RMStotal"@nl ;
    rdfs:comment "Rekenkundig gemiddelde van de minuutwaarden met resultaattijd in het lokale uur [hh:00, hh+1:00). Ontbrekende minuten tellen niet mee; het aantal staat bij de waarneming."@nl ;
    sosa:hasInput ex:prop-RMStotal ;
    sosa:hasOutput ex:prop-RMStotal .

ex:procedure-daggemiddelde a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Daggemiddelde van RMStotal"@nl ;
    rdfs:comment "Rekenkundig gemiddelde van de uurgemiddelden van de lokale dag: elk uur met metingen weegt even zwaar, ook als er minuten ontbreken (tijdgewogen gemiddelde). Het jaargemiddelde van de business case volgt op dezelfde manier uit de daggemiddelden."@nl ;
    sosa:hasInput ex:prop-RMStotal ;
    sosa:hasOutput ex:prop-RMStotal .

ex:prop-stroombelasting a sosa:Property ;
    rdfs:label "stroombelasting"@nl ;
    skos:definition "Elektrische stroom door de geleiders van een hoogspanningsverbinding of -station. Bepaalt het magnetische veld in de omgeving; de business case wil ze tonen als duiding bij de jaargemiddelde blootstelling. Geen data in dit voorbeeld."@nl ;
    qudt:hasQuantityKind quantitykind:ElectricCurrent .
"""]
    for k, label, definitie in METINGEN:
        out.append(f"""ex:prop-{k} a sosa:Property ;
    rdfs:label {lit(label)}@nl ;
    skos:notation {lit(k)} ;
    skos:definition {lit(definitie)}@nl ;
    qudt:hasQuantityKind quantitykind:MagneticFluxDensity .
""")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Telemetrie en indicatoren
# ---------------------------------------------------------------------------

def lees_metingen() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET, columns=["device", "tijdstip", "key", "dbl_v"])
    df = df[df.key.isin(SLEUTELS)]
    breed = df.pivot_table(index=["device", "tijdstip"], columns="key", values="dbl_v").reset_index()
    breed["lokaal"] = breed.tijdstip.dt.tz_convert(LOKAAL)
    breed["uur"] = breed.lokaal.dt.floor("h")
    return breed


def interval(iid: str, begin: pd.Timestamp, einde: pd.Timestamp) -> str:
    return f"""ex:interval-{iid} a time:Interval ;
    time:hasBeginning ex:instant-{iid}-begin ;
    time:hasEnd ex:instant-{iid}-einde .
ex:instant-{iid}-begin a time:Instant ;
    time:inXSDDateTimeStamp {lit(begin.isoformat())}^^xsd:dateTimeStamp .
ex:instant-{iid}-einde a time:Instant ;
    time:inXSDDateTimeStamp {lit(einde.isoformat())}^^xsd:dateTimeStamp .
"""


def indicator(oid: str, label: str, commentaar: str, procedure: str, locatie: str, iid: str,
              waarde: float, invoer: list[str], verwant: list[str]) -> str:
    return f"""ex:obs-{oid} a sosa:Observation ;
    rdfs:label {lit(label)}@nl ;
    rdfs:comment {lit(commentaar)}@nl ;
    sosa:madeBySensor ex:conversiescript ;
    sosa:usedProcedure ex:{procedure} ;
    sosa:observedProperty ex:prop-RMStotal ;
    sosa:hasFeatureOfInterest ex:meetlocatie-{locatie} ;
    sosa:phenomenonTime ex:interval-{iid} ;
    sosa:hasInputValue {" ,\n        ".join(invoer)} ;
    sosa:relatedObservation {" ,\n        ".join(verwant)} ;
    sosa:hasResult ex:result-{oid} .

ex:result-{oid} a qudt:QuantityValue ;
    qudt:numericValue {num(waarde)} ;
    qudt:hasUnit unit:MicroT .
"""


def uur_ttl(sensor: str, locatie: str, uur: pd.Timestamp, rijen: pd.DataFrame) -> tuple[str, dict]:
    """Minuutwaarden van één uur en de drie uurindicatoren. Geeft ook de uurwaarden terug voor de dag."""
    uid = f"{sensor}-{uur.strftime('%Y%m%dT%H')}"
    eind = uur + pd.Timedelta(hours=1)
    periode = f"{uur.strftime('%Y-%m-%d %H:00')}–{eind.strftime('%H:00')}"
    leden = [f"ex:meting-{sensor}-{ts_id(t)}" for t in rijen.tijdstip]
    out = [f"""# --- uur {periode} lokale tijd: {len(rijen)} meetmomenten ---

ex:collectie-{uid} a sosa:ObservationCollection ;
    rdfs:label {lit(f"Minuutwaarden {sensor}, {periode}")}@nl ;
    sosa:madeBySensor ex:sensor-{sensor} ;
    sosa:usedProcedure ex:procedure-elf-meting ;
    sosa:hasFeatureOfInterest ex:meetlocatie-{locatie} ;
    sosa:hasMember {" ,\n        ".join(leden)} .
"""]
    rms_res, rms_obs = [], []
    for _, r in rijen.iterrows():
        mid = f"{sensor}-{ts_id(r.tijdstip)}"
        obs = [f"ex:obs-{mid}-{k}" for k in SLEUTELS]
        out.append(f"""ex:meting-{mid} a sosa:ObservationCollection ;
    sosa:resultTime {lit(ts_utc(r.tijdstip))}^^xsd:dateTimeStamp ;
    sosa:hasMember {" , ".join(obs)} .
""")
        for k in SLEUTELS:
            out.append(f"""ex:obs-{mid}-{k} a sosa:Observation ; sosa:observedProperty ex:prop-{k} ; sosa:hasFeatureOfInterest ex:meetlocatie-{locatie} ; sosa:hasResult ex:result-{mid}-{k} .
ex:result-{mid}-{k} a qudt:QuantityValue ; qudt:numericValue {num(r[k])} ; qudt:hasUnit unit:MicroT .""")
        out.append("")
        rms_res.append(f"ex:result-{mid}-RMStotal")
        rms_obs.append(f"ex:obs-{mid}-RMStotal")

    waarden = {"minimum": rijen["RMStotal"].min(), "maximum": rijen["RMStotal"].max(),
               "gemiddelde": rijen["RMStotal"].mean()}
    out.append(f"# Uurindicatoren (R13): afgeleide waarnemingen buiten de collectie, met inputwaarden naar de minuutresultaten.\n")
    for stat, proc_uur, _ in INDICATOREN:
        out.append(indicator(f"{uid}-{stat}", f"Uur{stat} RMStotal {sensor}, {periode}",
                             f"Uit {len(rijen)} minuutwaarden.", proc_uur, locatie, uid,
                             waarden[stat], rms_res, rms_obs))
    out.append(interval(uid, uur, eind))
    return "\n".join(out), {"uid": uid, "waarden": waarden}


def dag_ttl(sensor: str, locatie: str, dag: pd.Timestamp, uren: list[dict]) -> str:
    did = f"{sensor}-{dag.strftime('%Y%m%d')}"
    einde = (dag.tz_localize(None) + pd.Timedelta(days=1)).tz_localize(LOKAAL)  # volgende lokale middernacht, ook bij zomertijdwissel
    out = [f"# --- dag {dag.strftime('%Y-%m-%d')}: dagindicatoren uit {len(uren)} uurindicatoren (afgeleide van afgeleiden) ---\n"]
    reductie = {"minimum": min, "maximum": max, "gemiddelde": lambda v: sum(v) / len(v)}
    for stat, _, proc_dag in INDICATOREN:
        waarde = reductie[stat]([u["waarden"][stat] for u in uren])
        out.append(indicator(f"{did}-{stat}", f"Dag{stat} RMStotal {sensor}, {dag.strftime('%Y-%m-%d')}",
                             f"Uit {len(uren)} {MEERVOUD[stat]}.", proc_dag, locatie, did, waarde,
                             [f"ex:result-{u['uid']}-{stat}" for u in uren],
                             [f"ex:obs-{u['uid']}-{stat}" for u in uren]))
    out.append(interval(did, dag, einde))
    return "\n".join(out)


def observaties(metingen: pd.DataFrame, campagne: dict, uren, dag=None) -> str:
    out = ["""###############################################################################
### OBSERVATIES
###############################################################################
# Per lokaal uur een sosa:ObservationCollection met sensor, procedure en studieobject; daarin per
# meetmoment een collectie met het resultaattijdstip (UTC, zoals ThingsBoard het geeft) en zeven
# observaties, één per sleutel. Leden erven wat de collecties vermelden (SOSA 2023, ExecutionCollection);
# sosa:hasFeatureOfInterest staat toch op elk lid, omdat de uit de OWL-restrictie op sosa:Execution
# gegenereerde SHACL de overerving niet ziet.
"""]
    sensor, locatie = campagne["sensor"], campagne["locatie"]
    uurwaarden = []
    for uur in uren:
        rijen = metingen[(metingen.device == sensor) & (metingen.uur == uur)].sort_values("tijdstip")
        if len(rijen):
            tekst, u = uur_ttl(sensor, locatie, uur, rijen)
            out.append(tekst)
            uurwaarden.append(u)
    if dag is not None:
        out.append(dag_ttl(sensor, locatie, dag, uurwaarden))
    return "\n".join(out)


def schrijf(pad: Path, kop: str, delen) -> None:
    pad.write_text(kop + "\n" + PREFIXEN + "\n" + "\n".join(delen), encoding="utf-8")
    print(f"{pad.name}: {pad.stat().st_size // 1024} kB")


def main():
    campagnes = lees_registratie()
    metingen = lees_metingen()
    hoofd = next(c for c in campagnes if c["ticket"] == "SENS-269")

    dagbegin = pd.Timestamp(datetime.combine(VOLLEDIGE_DAG, datetime.min.time(), LOKAAL))
    dag_uren = [dagbegin + pd.Timedelta(hours=h) for h in range(24)]
    schrijf(BASIS / "elf.trig",
            "# Gegenereerd door scripts/elf_to_rdf.py — niet met de hand wijzigen.\n"
            f"# ELF-meetnet: alle meetcampagnes uit de registratie, minuutwaarden van ELF_C_0020 op {VOLLEDIGE_DAG} "
            "(lokale dag) met uur- en dagindicatoren.\n"
            "# Gepseudonimiseerde bron; bronnen en geometrieën zijn fictief.",
            [infrastructuur(campagnes), campagnes_ttl(campagnes), procedures(),
             observaties(metingen, hoofd, dag_uren, dagbegin)])

    subset = [c for c in campagnes if c["ticket"] in VALIDATIE_CAMPAGNES]
    schrijf(BASIS / "elf.ttl",
            "# Gegenereerd door scripts/elf_to_rdf.py — niet met de hand wijzigen.\n"
            f"# Validatie-subset: meetcampagnes {', '.join(VALIDATIE_CAMPAGNES)}, minuutwaarden van ELF_C_0020 "
            f"van {VALIDATIE_UUR.strftime('%Y-%m-%d %H:00')} tot {(VALIDATIE_UUR + timedelta(hours=1)).strftime('%H:00')} "
            "lokale tijd met de uurindicatoren.\n"
            "# Gepseudonimiseerde bron; bronnen en geometrieën zijn fictief.",
            [infrastructuur(subset), campagnes_ttl(subset), procedures(),
             observaties(metingen, hoofd, [pd.Timestamp(VALIDATIE_UUR)])])


if __name__ == "__main__":
    main()
