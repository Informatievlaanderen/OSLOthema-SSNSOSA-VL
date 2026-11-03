#!/usr/bin/env python3
"""Zet de ELF-meetgegevens (ThingsBoard-export) en de sensorregistratie (Jira) om naar SSN/SOSA 2023.

Invoer  : source/_meetperiode_SENS-269_ELF_C_0020_<gemeente>.parquet  (gepseudonimiseerd, scripts/anonimiseer.py)
              telemetrie van ELF-node ELF_C_0020 in sleutel-waardevorm (één rij per tijdstip en sleutel)
          source/elf_sensors_registratie.csv
              Jira-export (project SENS): één ticket per meetcampagne (sensor, adres, start, einde)
Uitvoer : elf.trig  — één volledige lokale dag (VOLLEDIGE_DAG), alle meetcampagnes uit de registratie
                      (Turtle-inhoud; uitgesloten van de bulkvalidatie)
          elf.ttl   — validatie-subset: één uur (VALIDATIE_UUR) en de campagnes in VALIDATIE_CAMPAGNES

Gebruik : python3 scripts/elf_to_rdf.py   (vanuit src/main/input/elf/; vereist pandas en pyarrow)

Persoonsgegevens (contactpersoon, naam, voornaam) uit de registratie worden niet overgenomen.
De apparaatstatus (lastConnectTime, lastActivityTime, …, active, inactivityTimeout) wordt niet omgezet:
het zijn gegevens over de verbinding van het apparaat met ThingsBoard, geen waarnemingen van het veld.
"""
import csv
import re
from datetime import date, datetime, timedelta, timezone
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

MAANDEN = {"jan": 1, "feb": 2, "mrt": 3, "apr": 4, "mei": 5, "jun": 6,
           "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12}

PREFIXEN = """@prefix sosa:         <http://www.w3.org/ns/sosa/> .
@prefix prov:         <http://www.w3.org/ns/prov#> .
@prefix time:         <http://www.w3.org/2006/time#> .
@prefix qudt:         <http://qudt.org/schema/qudt/> .
@prefix unit:         <http://qudt.org/vocab/unit/> .
@prefix quantitykind: <http://qudt.org/vocab/quantitykind/> .
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


def ts_utc(t: pd.Timestamp) -> str:
    """xsd:dateTimeStamp in UTC, zoals de bron (milliseconden behouden)."""
    return t.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def ts_id(t: pd.Timestamp) -> str:
    """Deterministisch IRI-fragment uit het tijdstip (UTC, met milliseconden)."""
    return t.tz_convert("UTC").strftime("%Y%m%dT%H%M%S") + f"{t.microsecond // 1000:03d}Z"


def lokaal_stamp(d: datetime) -> str:
    return d.isoformat()


def jira_datum(s: str) -> datetime:
    """'26/nov/25 12:00 AM' → middernacht lokale tijd (de registratie bevat enkel datums)."""
    dag, maand, rest = s.strip().split("/", 2)
    jaar = int(rest.split()[0]) + 2000
    return datetime(jaar, MAANDEN[maand.lower()], int(dag), tzinfo=LOKAAL)


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
            })
    return campagnes


def infrastructuur(campagnes) -> str:
    out = []
    sensoren = sorted({c["sensor"] for c in campagnes})
    locaties = {}
    for c in campagnes:
        locaties.setdefault(c["locatie"], (c["adres"], c["gemeente"], []))[2].append(c["ticket"])

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
    sosa:observes {" , ".join("ex:prop-" + k for k in SLEUTELS)} ;
    sosa:hasDeployment {" , ".join("ex:meetcampagne-" + c["ticket"] for c in mijn)} .
""")
    for loc, (adres, gemeente, tickets) in sorted(locaties.items()):
        out.append(f"""ex:meetlocatie-{loc} a sosa:Platform , sosa:FeatureOfInterest ;
    rdfs:label {lit("Meetlocatie " + adres)}@nl ;
    rdfs:comment "De plaats waar de ELF-meter opgesteld staat en waarvan het magnetische veld bestudeerd wordt. Geen coördinaten in de bron; de positie volgt uit het adres."@nl ;
    prov:atLocation ex:adres-{loc} ;
    sosa:hasProperty {" , ".join("ex:prop-" + k for k in SLEUTELS)} ;
    sosa:inDeployment {" , ".join("ex:meetcampagne-" + t for t in tickets)} .

ex:adres-{loc} a prov:Location ;
    rdfs:label {lit(adres)}@nl .
""")
    out.append("""ex:conversiescript a sosa:Sensor , sosa:System ;
    rdfs:label "Conversiescript elf_to_rdf.py"@nl ;
    rdfs:comment "Software die de uurgemiddelden berekent uit de minuutwaarden. De uurgemiddelden staan niet in de bron: ze illustreren een afgeleide waarneming (R13)."@nl ;
    sosa:implements ex:procedure-uurgemiddelde .
""")
    return "\n".join(out)


def campagnes_ttl(campagnes) -> str:
    out = ["""###############################################################################
### MEETCAMPAGNES (sosa:Deployment)
###############################################################################
# Eén Jira-ticket = één meetcampagne. Start en einde uit de registratie (enkel datums, middernacht
# lokale tijd). Een einde na de peildatum is een gepland einde en wordt niet als prov:endedAtTime
# opgenomen.
"""]
    for c in campagnes:
        regels = [f"""ex:meetcampagne-{c["ticket"]} a sosa:Deployment ;
    rdfs:label {lit(f'Meetcampagne {c["ticket"]}: {c["sensor"]} op {c["adres"]}')}@nl ;
    dcterms:identifier {lit(c["ticket"])} ;
    sosa:deployedSystem ex:sensor-{c["sensor"]} ;
    sosa:deployedOnPlatform ex:meetlocatie-{c["locatie"]} ;
    sosa:hasFeatureOfInterest ex:meetlocatie-{c["locatie"]} ;
    prov:startedAtTime {lit(lokaal_stamp(c["start"]))}^^xsd:dateTime"""]
        if c["einde"].date() <= PEILDATUM:
            regels.append(f"""    prov:endedAtTime {lit(lokaal_stamp(c["einde"]))}^^xsd:dateTime""")
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
    sosa:hasOutput """ + " , ".join("ex:prop-" + k for k in SLEUTELS) + """ .

ex:procedure-uurgemiddelde a sosa:ObservingProcedure , sosa:Procedure ;
    rdfs:label "Rekenkundig uurgemiddelde van RMStotal"@nl ;
    rdfs:comment "Rekenkundig gemiddelde van de RMStotal-waarden waarvan het resultaattijdstip in het lokale uur [hh:00, hh+1:00) valt. Uren met ontbrekende minuten worden gemiddeld over de beschikbare waarden."@nl ;
    sosa:hasInput ex:prop-RMStotal ;
    sosa:hasOutput ex:prop-RMStotal .
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
# Telemetrie
# ---------------------------------------------------------------------------

def lees_metingen() -> pd.DataFrame:
    df = pd.read_parquet(PARQUET, columns=["device", "tijdstip", "key", "dbl_v"])
    df = df[df.key.isin(SLEUTELS)]
    breed = df.pivot_table(index=["device", "tijdstip"], columns="key", values="dbl_v").reset_index()
    breed["lokaal"] = breed.tijdstip.dt.tz_convert(LOKAAL)
    breed["uur"] = breed.lokaal.dt.floor("h")
    return breed


def num(v: float) -> str:
    s = f"{v:.5f}".rstrip("0").rstrip(".")
    return s if "." in s else s + ".0"


def uur_ttl(sensor: str, campagne: str, locatie: str, uur: pd.Timestamp, rijen: pd.DataFrame) -> str:
    uid = uur.strftime("%Y%m%dT%H")
    coll = f"ex:collectie-{sensor}-{uid}"
    eind = uur + pd.Timedelta(hours=1)
    leden = [f"ex:meting-{sensor}-{ts_id(t)}" for t in rijen.tijdstip]
    out = [f"""# --- uur {uur.strftime('%Y-%m-%d %H:00')}–{eind.strftime('%H:00')} lokale tijd: {len(rijen)} meetmomenten ---

{coll} a sosa:ObservationCollection ;
    rdfs:label {lit(f"Minuutwaarden {sensor}, {uur.strftime('%Y-%m-%d %H:00')}–{eind.strftime('%H:00')}")}@nl ;
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

    gem = rijen["RMStotal"].mean()
    did = f"{sensor}-{uid}-uurgemiddelde"
    out.append(f"""# Afgeleide waarneming (R13): buiten de collectie, met inputwaarden naar de resultaten.
ex:obs-{did} a sosa:Observation ;
    rdfs:label {lit(f"Uurgemiddelde RMStotal {sensor}, {uur.strftime('%Y-%m-%d %H:00')}–{eind.strftime('%H:00')}")}@nl ;
    rdfs:comment {lit(f"Gemiddelde van {len(rijen)} minuutwaarden.")}@nl ;
    sosa:madeBySensor ex:conversiescript ;
    sosa:usedProcedure ex:procedure-uurgemiddelde ;
    sosa:observedProperty ex:prop-RMStotal ;
    sosa:hasFeatureOfInterest ex:meetlocatie-{locatie} ;
    sosa:phenomenonTime ex:interval-{did} ;
    sosa:hasInputValue {" ,\n        ".join(rms_res)} ;
    sosa:relatedObservation {" ,\n        ".join(rms_obs)} ;
    sosa:hasResult ex:result-{did} .

ex:result-{did} a qudt:QuantityValue ;
    qudt:numericValue {num(gem)} ;
    qudt:hasUnit unit:MicroT .

ex:interval-{did} a time:Interval ;
    time:hasBeginning ex:instant-{did}-begin ;
    time:hasEnd ex:instant-{did}-einde .
ex:instant-{did}-begin a time:Instant ;
    time:inXSDDateTimeStamp {lit(uur.isoformat())}^^xsd:dateTimeStamp .
ex:instant-{did}-einde a time:Instant ;
    time:inXSDDateTimeStamp {lit(eind.isoformat())}^^xsd:dateTimeStamp .
""")
    return "\n".join(out)


def observaties(metingen: pd.DataFrame, campagne: dict, uren) -> str:
    out = ["""###############################################################################
### OBSERVATIES
###############################################################################
# Per lokaal uur een sosa:ObservationCollection met sensor, procedure en studieobject; daarin per
# meetmoment een collectie met het resultaattijdstip (UTC, zoals ThingsBoard het geeft) en zeven
# observaties, één per sleutel. Leden erven wat de collecties vermelden (SOSA 2023, ExecutionCollection);
# sosa:hasFeatureOfInterest staat toch op elk lid, omdat de uit de OWL-restrictie op sosa:Execution
# gegenereerde SHACL de overerving niet ziet.
"""]
    sensor = campagne["sensor"]
    for uur in uren:
        rijen = metingen[(metingen.device == sensor) & (metingen.uur == uur)].sort_values("tijdstip")
        if len(rijen):
            out.append(uur_ttl(sensor, campagne["ticket"], campagne["locatie"], uur, rijen))
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
            f"# ELF-meetnet: alle meetcampagnes uit de registratie, minuutwaarden van ELF_C_0020 op {VOLLEDIGE_DAG} (lokale dag).",
            [infrastructuur(campagnes), campagnes_ttl(campagnes), procedures(),
             observaties(metingen, hoofd, dag_uren)])

    subset = [c for c in campagnes if c["ticket"] in VALIDATIE_CAMPAGNES]
    schrijf(BASIS / "elf.ttl",
            "# Gegenereerd door scripts/elf_to_rdf.py — niet met de hand wijzigen.\n"
            f"# Validatie-subset: meetcampagnes {', '.join(VALIDATIE_CAMPAGNES)}, minuutwaarden van ELF_C_0020 "
            f"van {VALIDATIE_UUR.strftime('%Y-%m-%d %H:00')} tot {(VALIDATIE_UUR + timedelta(hours=1)).strftime('%H:00')} lokale tijd.",
            [infrastructuur(subset), campagnes_ttl(subset), procedures(),
             observaties(metingen, hoofd, [pd.Timestamp(VALIDATIE_UUR)])])


if __name__ == "__main__":
    main()
