"""Stap 2 van stappenplan.md: concentraties in oppervlaktewater (250114) naar SSN/SOSA 2023.

Invoer:
- ../brondata_Jurgen/250114_Analyseresultaten_per_meetplaats_OW/Resultaten.json en SamplePoints.json
- ../waterlopen/meetplaats_waterloop.csv (koppeling meetplaats -> VHA-waterloop, waterlopen_subset.py)
- ../waterlopen/waterlopen_meetplaatsen.ttl (beschrijving van de gekoppelde VHA-waterlopen, code:Vhag)
- CSOR-codelijsten in ~/git/csor (via waterkwaliteit_gemeen.Csor)

Uitvoer (../nieuw_model/oppervlaktewater_concentraties/):
- oppervlaktewater_concentraties.trig  alle resultaten (Turtle-inhoud, buiten de Maven-validatie)
- oppervlaktewater_concentraties.ttl   één staal (SUBSET_STAAL) als validatie-subset

Model (zie bespreking.md in de uitvoermap), R8/R11:
  VHA-waterloop (FOI, ultiem) <-isSampleOf- meetplaats (SpatialSample + Platform + FOI)
      <-isSampleOf- staal (Sample, FOI) <-hasResult- sampling
  De meetplaats is zelf het resultaat van een ruimtelijke bemonstering van de waterloop
  (sosa:Sampling, keuze van de meetplaats), zodat ook de waterloop FOI van een Execution is.
  collectie per staal -hasMember-> observatie per parameter (patroon van stap 1).

De bron heeft geen staal-ID en geen parametercode:
- staal = (Sample Point, datum, tijdstip); tijdstip afgerond op de seconde (Excel-artefact
  12:50:59.999 -> 12:51:00);
- parameter = CSOR-symbool + drager 'water' (eenduidig, ../../codelijsten.md §3.1).
Resultaatteken: '=' -> qudt:numericValue; '<' -> qudt:lowerBound 0 + qudt:upperBound (als stap 1).

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/oppervlaktewater_concentraties.py [--csor ~/git/csor]

Vereist: rdflib.
"""
import argparse
import collections
import csv
import datetime
import json
import os
import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from waterkwaliteit_gemeen import CSOR, EPSG31370, GEO, MATRIX, QUDT, SOSA, TIME, WK, Csor, decimaal  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
BRONMAP = os.path.normpath(os.path.join(HIER, "..", "brondata_Jurgen", "250114_Analyseresultaten_per_meetplaats_OW"))
KOPPELING = os.path.normpath(os.path.join(HIER, "..", "waterlopen", "meetplaats_waterloop.csv"))
VHA = os.path.normpath(os.path.join(HIER, "..", "waterlopen", "waterlopen_meetplaatsen.ttl"))
WATERLOPEN = Namespace("https://data.omgeving.vlaanderen.be/ns/waterlopen#")
UIT = os.path.normpath(os.path.join(HIER, "..", "nieuw_model", "oppervlaktewater_concentraties"))
NAAM = "oppervlaktewater_concentraties"
SUBSET_STAAL = ("OW12000", "2019-01-28", "13:01:00")
# Een volledig staal (331 resultaten) is te zwaar voor de OWL-validatie van de pipeline (minuten per
# bestand). De subset beperkt zich tot representatieve parameters: alle soorten eenheden en grootheden,
# en twee resultaten onder de rapportagegrens.
SUBSET_PARAMETERS = {"pH", "EC 20", "T", "O2 verz", "BZV5", "KjN", "NO3-", "P t", "H t", "Cl-",
                     "Zn o", "Cu o", "TBySn", "1112CEa"}

EX = Namespace("https://example.org/waterkwaliteit/oppervlaktewater/")
WATERLOOP = Namespace("https://data.omgeving.vlaanderen.be/id/waterloop/")


def tijdstip(datum, tijd):
    """Datum + tijd, afgerond op de seconde (Excel levert soms 12:50:59.999000)."""
    t = datetime.datetime.fromisoformat(f"{datum}T{tijd}")
    t = (t + datetime.timedelta(microseconds=500_000)).replace(microsecond=0)
    return t.isoformat()


def bouw(rijen, meetplaatsen, koppeling, csor, vha):
    g = Graph()
    for p, ns in (("ex", EX), ("sosa", SOSA), ("qudt", QUDT), ("time", TIME), ("geo", GEO), ("dct", DCTERMS),
                  ("skos", SKOS), ("xsd", XSD), ("rdfs", RDFS), ("waterloop", WATERLOOP),
                  ("waterlopen", WATERLOPEN),
                  ("csor-parameteraspect", "https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/"),
                  ("csor-eenheid", "https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/"), ("csor", CSOR),
                  ("matrix", MATRIX)):
        g.bind(p, ns)
    gezien = set()
    ontbrekend = collections.Counter()

    def label(iri, tekst):
        g.add((iri, RDFS.label, Literal(str(tekst), lang="nl")))

    matrix = MATRIX["oppervlaktewater"]
    g.add((matrix, RDF.type, SKOS.Concept))
    label(matrix, "Oppervlaktewater")

    for r in rijen:
        sp = r["Sample Point"]
        mp = meetplaatsen[sp]
        k = koppeling.get(sp)
        if k is None or not k["waterloop"]:
            sys.exit(f"meetplaats {sp} heeft geen VHA-waterloop in {KOPPELING}")
        tijd = tijdstip(r["Sample Datum Monstername"], r["Sample Tijdstip Monstername"])
        sleutel = f"{sp}-{tijd.replace(':', '')}"            # OW12000-2019-01-28T130100
        meetplaats, waterloop = EX[f"meetplaats-{sp}"], URIRef(k["waterloop"])
        keuze = EX[f"sampling-meetplaats-{sp}"]
        staal, sampling, collectie = EX[f"staal-{sleutel}"], EX[f"sampling-{sleutel}"], EX[f"collectie-{sleutel}"]
        moment = EX[f"tijdstip-{tijd.replace(':', '')}"]

        if sp not in gezien:
            gezien.add(sp)
            # VHA-waterloop (code:Vhag ⊂ sosa:FeatureOfInterest, waterkwaliteit.ttl; ⊂ geo:Feature,
            # waterlopen.ttl): de volledige beschrijving uit ../waterlopen/waterlopen_meetplaatsen.ttl,
            # met de geometrie (blank node), zodat de data conform is aan de VHA-shape (lengte,
            # geometrie) en het label dat van de VHA is.
            if (waterloop, RDF.type, WATERLOPEN.Vhag) not in vha:
                sys.exit(f"waterloop {waterloop} van meetplaats {sp} ontbreekt als code:Vhag in {VHA}")
            for p_, o_ in vha.predicate_objects(waterloop):
                g.add((waterloop, p_, o_))
                if p_ == GEO.hasGeometry:
                    for t in vha.triples((o_, None, None)):
                        g.add(t)
            g.add((waterloop, RDF.type, WATERLOPEN.VhaWaterloopobject))  # superklasse, expliciet voor SHACL
            g.add((waterloop, RDF.type, SOSA.FeatureOfInterest))
            g.add((waterloop, SOSA.hasSample, meetplaats))
            g.add((waterloop, SOSA.isFeatureOfInterestOf, keuze))
            # ruimtelijke bemonstering: keuze van de meetplaats op de waterloop
            g.add((keuze, RDF.type, SOSA.Sampling))
            g.add((keuze, RDF.type, SOSA.Execution))
            label(keuze, f"Keuze van meetplaats {sp} op {k['segment_naam']}")
            g.add((keuze, SOSA.hasFeatureOfInterest, waterloop))
            g.add((keuze, SOSA.hasResult, meetplaats))
            # meetplaats (R11)
            for typ in (SOSA.Platform, SOSA.FeatureOfInterest, SOSA.SpatialSample, SOSA.Sample):
                g.add((meetplaats, RDF.type, typ))
            g.add((meetplaats, RDF.type, WK.Meetplaats))  # AP (beslisdocument.md A15)
            label(meetplaats, sp)
            g.add((meetplaats, RDFS.comment, Literal(mp["Sample Point Omschrijving"], lang="nl")))
            g.add((meetplaats, SOSA.isSampleOf, waterloop))
            g.add((meetplaats, SOSA.isResultOf, keuze))
            geom = EX[f"geometrie-meetplaats-{sp}"]
            g.add((meetplaats, GEO.hasGeometry, geom))
            g.add((meetplaats, RDF.type, GEO.Feature))  # domein van geo:hasGeometry
            g.add((geom, RDF.type, GEO.Geometry))
            g.add((geom, GEO.asWKT, Literal(f"{EPSG31370} POINT({mp['Lambert X']} {mp['Lambert Y']})",
                                            datatype=GEO.wktLiteral)))

        g.add((moment, RDF.type, TIME.Instant))
        g.add((moment, TIME.inXSDDateTime, Literal(tijd, datatype=XSD.dateTime)))

        # bemonstering van het water op de meetplaats
        g.add((sampling, RDF.type, SOSA.Sampling))
        g.add((sampling, RDF.type, WK.Staalname))  # AP (beslisdocument.md A15)
        g.add((sampling, RDF.type, SOSA.Execution))
        g.add((sampling, SOSA.hasFeatureOfInterest, meetplaats))
        g.add((sampling, SOSA.hasResult, staal))
        g.add((sampling, SOSA.phenomenonTime, moment))
        g.add((meetplaats, SOSA.isFeatureOfInterestOf, sampling))
        g.add((meetplaats, SOSA.hasSample, staal))

        g.add((staal, RDF.type, SOSA.Sample))
        g.add((staal, RDF.type, WK.Staal))  # AP (beslisdocument.md A15)
        g.add((staal, RDF.type, SOSA.FeatureOfInterest))
        label(staal, f"Staal {sp} {tijd}")
        g.add((staal, DCTERMS.type, matrix))
        g.add((staal, SOSA.isSampleOf, meetplaats))
        g.add((staal, SOSA.isResultOf, sampling))
        g.add((staal, SOSA.isFeatureOfInterestOf, collectie))

        g.add((collectie, RDF.type, SOSA.ObservationCollection))
        g.add((collectie, RDF.type, WK.WaterkwaliteitObservatieVerzameling))  # AP (beslisdocument.md A15)
        g.add((collectie, RDF.type, SOSA.ExecutionCollection))
        label(collectie, f"Analyseresultaten staal {sp} {tijd}")
        g.add((collectie, SOSA.hasFeatureOfInterest, staal))
        g.add((collectie, SOSA.hasUltimateFeatureOfInterest, waterloop))
        g.add((collectie, SOSA.phenomenonTime, moment))

        # observatie en resultaat
        pa, eenheid = csor.parameteraspect_symbool(r["Parameter Symbool"], "water", r["Eenheid"])
        if pa is None or eenheid is None:
            ontbrekend[(r["Parameter Symbool"], r["Eenheid"])] += 1
            continue
        for iri, typen in ((pa, (SOSA.Property, CSOR.ParameterAspect)), (eenheid, (CSOR.Eenheid,))):
            if iri not in gezien:
                gezien.add(iri)
                for typ in typen:
                    g.add((iri, RDF.type, typ))
                label(iri, csor.label(iri))
        code = str(pa).rsplit("/", 1)[1]
        obs, res = EX[f"observatie-{sleutel}-{code}"], EX[f"resultaat-{sleutel}-{code}"]
        g.add((collectie, SOSA.hasMember, obs))
        g.add((obs, RDF.type, SOSA.Observation))
        g.add((obs, RDF.type, WK.WaterkwaliteitObservatie))  # AP (beslisdocument.md A15)
        g.add((obs, RDF.type, SOSA.Execution))
        g.add((obs, SOSA.hasFeatureOfInterest, staal))
        g.add((obs, SOSA.hasUltimateFeatureOfInterest, waterloop))
        g.add((obs, SOSA.observedProperty, pa))
        g.add((obs, SOSA.hasResult, res))
        g.add((res, RDF.type, SOSA.Result))
        g.add((res, RDF.type, WK.Meetresultaat))  # AP (beslisdocument.md A15)
        g.add((res, SOSA.isResultOf, obs))
        g.add((res, QUDT.hasUnit, eenheid))
        if r["Teken"] == "=":
            g.add((res, QUDT.numericValue, decimaal(r["Resultaat"])))
        elif r["Teken"] == "<":
            g.add((res, QUDT.lowerBound, decimaal(0)))
            g.add((res, QUDT.upperBound, decimaal(r["Resultaat"])))
        else:
            sys.exit(f"onbekend teken {r['Teken']!r} bij {sleutel}, {r['Parameter Symbool']}")
    return g, ontbrekend


def schrijf(g, pad, kop):
    with open(pad, "w", encoding="utf-8") as f:
        f.write(kop + g.serialize(format="turtle"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csor", default="~/git/csor", help="map met de codelijst-csor-*-repo's")
    args = ap.parse_args()

    rijen = json.load(open(os.path.join(BRONMAP, "Resultaten.json"), encoding="utf-8"))
    meetplaatsen = {r["Sample Point"]: r for r in json.load(open(os.path.join(BRONMAP, "SamplePoints.json"),
                                                                  encoding="utf-8"))}
    koppeling = {r["sample_point"]: r for r in csv.DictReader(open(KOPPELING, encoding="utf-8"))}
    csor = Csor(args.csor)
    vha = Graph().parse(VHA, format="turtle")
    os.makedirs(UIT, exist_ok=True)

    kop = ("# Concentraties in oppervlaktewater (VMM, 250114) als SSN/SOSA 2023 -- DIT IS VOORBEELDDATA\n"
           "# Gegenereerd door scripts/oppervlaktewater_concentraties.py; niet manueel bewerken.\n")
    volledig, ontbrekend = bouw(rijen, meetplaatsen, koppeling, csor, vha)
    schrijf(volledig, os.path.join(UIT, f"{NAAM}.trig"), kop)
    sp, datum, tijd = SUBSET_STAAL
    subset, _ = bouw([r for r in rijen if (r["Sample Point"], r["Sample Datum Monstername"],
                                           r["Sample Tijdstip Monstername"]) == SUBSET_STAAL
                      and r["Parameter Symbool"] in SUBSET_PARAMETERS],
                     meetplaatsen, koppeling, csor, vha)
    schrijf(subset, os.path.join(UIT, f"{NAAM}.ttl"), kop + f"# Validatie-subset: staal {sp} {datum} {tijd}, "
            f"{len(SUBSET_PARAMETERS)} representatieve parameters.\n")

    print(f"{len(rijen)} rijen -> {len(set(volledig.subjects(RDF.type, SOSA.Observation)))} observaties, "
          f"{len(set(volledig.subjects(RDF.type, SOSA.ObservationCollection)))} stalen; {len(volledig)} triples; "
          f"subset {len(subset)} triples", file=sys.stderr)
    if ontbrekend:
        print(f"zonder CSOR-parameteraspect of -eenheid: {dict(ontbrekend)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
