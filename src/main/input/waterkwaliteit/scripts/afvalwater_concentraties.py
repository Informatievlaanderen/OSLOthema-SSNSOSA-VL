"""Stap 1 van stappenplan.md: concentraties in afvalwater (250108) naar SSN/SOSA 2023.

Invoer:
- ../brondata_Jurgen/250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024/Pagina1.json
- CSOR-codelijsten (parameter, parameteraspect, kwantificeerbaar aspect, eenheid) in ~/git/csor
- ../brondata_Jurgen/Lijst_observatiemethodes_VITO-v1/Observatiemethoden.json: jaarversies van de
  observatieprocedures (VITO, v1). De staalname verwijst naar de versie van het jaar van de
  staalname (bv. WAC_I_A_003_2024), met dct:isVersionOf naar de hoofdprocedure.

Uitvoer (../nieuw_model/afvalwater_concentraties/):
- afvalwater_concentraties.trig  alle 1998 resultaten (Turtle-inhoud, buiten de Maven-validatie)
- afvalwater_concentraties.ttl   één staal (SUBSET_STAAL) als validatie-subset

Model (zie bespreking.md in de uitvoermap):
  lozing (FOI, ultiem) <-isSampleOf- staal (Sample, FOI) <-hasResult- sampling (Sampling)
  collectie per staal (ObservationCollection) -hasMember-> observatie per parameter
  observatie -observedProperty-> CSOR-parameteraspect; -hasResult-> resultaat
  resultaat: qudt:numericValue (teken '=') of qudt:lowerBound/upperBound (teken '<'),
             qudt:hasUnit -> CSOR-eenheid

Afgeleide supertypes (sosa:Execution, sosa:ExecutionCollection, sosa:FeatureOfInterest op het
staal) worden expliciet toegevoegd: de pipeline valideert SHACL op het niet-geïnfereerde model.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/afvalwater_concentraties.py [--csor ~/git/csor]

Vereist: rdflib.
"""
import argparse
import collections
import json
import os
import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, PROV, RDF, RDFS, SKOS, XSD

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from waterkwaliteit_gemeen import (ADMS, CSOR, EPSG31370, GEO, MATRIX, PROCEDURE as OBSPROC, QUDT, SOSA,  # noqa: E402
                                   TIME, WK, Csor, Procedures, decimaal)

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.normpath(os.path.join(
    HIER, "..", "brondata_Jurgen", "250108_AW_Resultaat_Prompts_R_62-mtpn-UK-PFAS-AW_2024", "Pagina1.json"))
UIT = os.path.normpath(os.path.join(HIER, "..", "nieuw_model", "afvalwater_concentraties"))
NAAM = "afvalwater_concentraties"
SUBSET_STAAL = "16231"  # M-AW-2024-006358-1, RWZI Mechelen-Noord: 15 resultaten, teken '<' en '='

EX = Namespace("https://example.org/waterkwaliteit/afvalwater/")

# Soort monstername -> hoofdprocedure (WAC). "Debietgebonden monster" = verzamelmonster: te
# bevestigen door de VMM (stappenplan.md V1). De jaarversie wordt per staal gekozen (Procedures).
MONSTERNAME = {
    "Schepmonster": OBSPROC["WAC_I_A_003"],
    "Debietgebonden monster": OBSPROC["WAC_I_A_004"],
}
MATRICES = {"Afvalwater": MATRIX["afvalwater"]}


def bouw(rijen, csor, procedures):
    g = Graph()
    for p, ns in (("ex", EX), ("sosa", SOSA), ("qudt", QUDT), ("time", TIME), ("geo", GEO), ("adms", ADMS),
                  ("prov", PROV), ("dct", DCTERMS), ("skos", SKOS), ("xsd", XSD), ("rdfs", RDFS),
                  ("csor-parameteraspect", "https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/"),
                  ("csor-eenheid", "https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/"), ("csor", CSOR),
                  ("matrix", MATRIX), ("procedure", OBSPROC), ("wk", WK)):
        g.bind(p, ns)

    vmm = EX["organisatie-vmm"]
    g.add((vmm, RDF.type, PROV.Organization))
    g.add((vmm, RDF.type, PROV.Agent))  # AP (beslisdocument.md A15)
    g.add((vmm, RDFS.label, Literal("Vlaamse Milieumaatschappij", lang="nl")))

    ontbrekend = collections.Counter()
    gezien_extern = set()

    def extern(iri, typen, label):
        """Minimale type-assertie en label voor een externe concept-IRI (CSOR, WAC, matrix)."""
        if iri not in gezien_extern:
            gezien_extern.add(iri)
            for typ in typen:
                g.add((iri, RDF.type, typ))
            if label is not None:
                g.add((iri, RDFS.label, Literal(str(label), lang="nl")))

    for r in rijen:
        nr = r["Sample Point Naam"][2:]          # AW2800028 -> 2800028 = VMM-meetputnummer (V4)
        sid = str(r["Sample ID"])
        code = r["Parameter Code"]
        meetpunt, lozing = EX[f"meetpunt-{nr}"], EX[f"lozing-{nr}"]
        exploitatie = EX[f"exploitatie-{r['Exploitatie ID']}"]
        staal, sampling, collectie = EX[f"staal-{sid}"], EX[f"sampling-{sid}"], EX[f"collectie-{sid}"]
        tijdstip = EX[f"tijdstip-{r['Datum Dag']}"]
        obs, res = EX[f"observatie-{sid}-{code}"], EX[f"resultaat-{sid}-{code}"]

        # --- structuur (idempotent: rdflib-graaf negeert dubbele triples) ---
        g.add((exploitatie, RDF.type, PROV.Organization))
        g.add((exploitatie, RDF.type, PROV.Agent))  # AP (beslisdocument.md A15)
        g.add((exploitatie, RDFS.label, Literal(r["Exploitatie Naam"].strip(), lang="nl")))
        g.add((exploitatie, DCTERMS.identifier, Literal(str(r["Exploitatie ID"]))))

        g.add((meetpunt, RDF.type, SOSA.Sampler))
        g.add((meetpunt, RDF.type, WK.Meetput))  # AP (beslisdocument.md A15)
        g.add((meetpunt, RDF.type, PROV.Location))  # AP (beslisdocument.md A15)
        g.add((meetpunt, RDFS.label, Literal(r["Sample Point Naam"], lang="nl")))
        g.add((meetpunt, RDFS.comment, Literal(r["Sample Point Omschrijving"].strip(), lang="nl")))
        ident = EX[f"identificator-meetpunt-{nr}"]
        g.add((meetpunt, ADMS.identifier, ident))
        g.add((ident, RDF.type, ADMS.Identifier))
        g.add((ident, SKOS.notation, Literal(nr)))
        g.add((ident, DCTERMS.creator, vmm))
        geom = EX[f"geometrie-meetpunt-{nr}"]
        g.add((meetpunt, GEO.hasGeometry, geom))
        g.add((meetpunt, RDF.type, GEO.Feature))  # domein van geo:hasGeometry
        g.add((geom, RDF.type, GEO.Geometry))
        x, y = r["Sample Point Lambert72 X Coördinaat"], r["Sample Point Lambert72 Y Coördinaat"]
        g.add((geom, GEO.asWKT, Literal(f"{EPSG31370} POINT({x} {y})", datatype=GEO.wktLiteral)))

        g.add((lozing, RDF.type, WK.Emissie))           # beslisdocument.md A14
        g.add((lozing, RDF.type, SOSA.FeatureOfInterest))
        g.add((lozing, RDF.type, PROV.Entity))
        g.add((lozing, RDFS.label, Literal(f"Lozing aan meetput {r['Sample Point Naam']} "
                                           f"({r['Exploitatie Naam'].strip()})", lang="nl")))
        g.add((lozing, PROV.wasAttributedTo, exploitatie))
        g.add((lozing, SOSA.hasSample, staal))
        g.add((lozing, SOSA.isFeatureOfInterestOf, sampling))

        g.add((tijdstip, RDF.type, TIME.Instant))
        g.add((tijdstip, TIME.inXSDDate, Literal(r["Datum Dag"], datatype=XSD.date)))

        # --- bemonstering ---
        hoofd = MONSTERNAME[r["Aard Monstername"]]
        versie = procedures.voor(hoofd, int(r["Datum Dag"][:4]))
        procedure = URIRef(versie["URI"])
        if procedure not in gezien_extern:
            extern(procedure, (SOSA.SamplingProcedure, SOSA.Procedure, SKOS.Concept), versie["Pref_label"])
            g.add((procedure, DCTERMS.isVersionOf, hoofd))
            g.add((procedure, DCTERMS.issued, Literal(str(versie["Jaar"]), datatype=XSD.gYear)))
            if versie["pdf-bestand"]:
                g.add((procedure, PROV.hadPrimarySource, URIRef(versie["pdf-bestand"])))
            extern(hoofd, (SOSA.SamplingProcedure, SOSA.Procedure, SKOS.Concept),
                   procedures.hoofd[hoofd]["Pref_label"])
        g.add((sampling, RDF.type, SOSA.Sampling))
        g.add((sampling, RDF.type, WK.Staalname))  # AP (beslisdocument.md A15)
        g.add((sampling, RDF.type, SOSA.Execution))
        g.add((sampling, SOSA.hasFeatureOfInterest, lozing))
        g.add((sampling, SOSA.madeBySampler, meetpunt))
        g.add((sampling, SOSA.usedProcedure, procedure))
        g.add((sampling, SOSA.phenomenonTime, tijdstip))
        g.add((sampling, SOSA.hasResult, staal))
        uitvoerder = vmm if r["Sample Type Staal Code"] == "VMM" else exploitatie   # BEDR = staal bedrijf
        g.add((sampling, PROV.wasAssociatedWith, uitvoerder))

        g.add((staal, RDF.type, SOSA.Sample))
        g.add((staal, RDF.type, WK.Staal))  # AP (beslisdocument.md A15)
        g.add((staal, RDF.type, SOSA.FeatureOfInterest))
        g.add((staal, RDFS.label, Literal(r["Sample ID Tekst"])))
        g.add((staal, DCTERMS.identifier, Literal(sid)))
        matrix = MATRICES[r["Matrix"]]
        extern(matrix, (SKOS.Concept,), r["Matrix"])
        g.add((staal, DCTERMS.type, matrix))
        g.add((lozing, DCTERMS.type, matrix))       # de lozing is afvalwater (tijdsloos FOI)
        g.add((staal, SOSA.isSampleOf, lozing))
        g.add((staal, SOSA.isResultOf, sampling))
        g.add((staal, SOSA.isFeatureOfInterestOf, collectie))

        g.add((collectie, RDF.type, SOSA.ObservationCollection))
        g.add((collectie, RDF.type, WK.WaterkwaliteitObservatieVerzameling))  # AP (beslisdocument.md A15)
        g.add((collectie, RDF.type, SOSA.ExecutionCollection))
        g.add((collectie, RDFS.label, Literal(f"Analyseresultaten staal {r['Sample ID Tekst']}", lang="nl")))
        g.add((collectie, SOSA.hasFeatureOfInterest, staal))
        g.add((collectie, SOSA.hasUltimateFeatureOfInterest, lozing))
        g.add((collectie, SOSA.phenomenonTime, tijdstip))
        g.add((collectie, SOSA.hasMember, obs))

        # --- observatie en resultaat ---
        pa, eenheid = csor.parameteraspect(code, r["Eenheid"])
        if pa is None or eenheid is None:
            ontbrekend[(code, r["Eenheid"])] += 1
            continue
        extern(pa, (SOSA.Property, CSOR.ParameterAspect), csor.label(pa))
        extern(eenheid, (CSOR.Eenheid,), csor.label(eenheid))
        g.add((obs, RDF.type, SOSA.Observation))
        g.add((obs, RDF.type, WK.WaterkwaliteitObservatie))  # AP (beslisdocument.md A15)
        g.add((obs, RDF.type, SOSA.Execution))
        g.add((obs, SOSA.hasFeatureOfInterest, staal))
        g.add((obs, SOSA.hasUltimateFeatureOfInterest, lozing))
        g.add((obs, SOSA.observedProperty, pa))
        g.add((obs, SOSA.hasResult, res))

        g.add((res, RDF.type, SOSA.Result))
        g.add((res, RDF.type, WK.Meetresultaat))  # AP (beslisdocument.md A15)
        g.add((res, SOSA.isResultOf, obs))
        g.add((res, QUDT.hasUnit, eenheid))
        waarde = r["Resultaat Standaard Eenheid"]
        if r["Resultaat Teken"] == "=":
            g.add((res, QUDT.numericValue, decimaal(waarde)))
        elif r["Resultaat Teken"] == "<":
            # onder de rapportagegrens: geen gemeten waarde, enkel het interval [0, grens]
            g.add((res, QUDT.lowerBound, decimaal(r["Resultaat Ondergrens Standaard Eenheid"])))
            g.add((res, QUDT.upperBound, decimaal(r["Resultaat Bovengrens Standaard Eenheid"])))
        else:
            sys.exit(f"onbekend teken {r['Resultaat Teken']!r} in staal {sid}, {code}")
    return g, ontbrekend


def schrijf(g, pad, kop):
    tekst = g.serialize(format="turtle")
    with open(pad, "w", encoding="utf-8") as f:
        f.write(kop + tekst)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csor", default="~/git/csor", help="map met de codelijst-csor-*-repo's")
    args = ap.parse_args()

    rijen = json.load(open(BRON, encoding="utf-8"))
    csor = Csor(args.csor)
    procedures = Procedures()
    os.makedirs(UIT, exist_ok=True)

    kop = ("# Concentraties in afvalwater (VMM, 250108) als SSN/SOSA 2023 -- DIT IS VOORBEELDDATA\n"
           "# Gegenereerd door scripts/afvalwater_concentraties.py; niet manueel bewerken.\n")
    volledig, ontbrekend = bouw(rijen, csor, procedures)
    schrijf(volledig, os.path.join(UIT, f"{NAAM}.trig"), kop)
    subset, _ = bouw([r for r in rijen if str(r["Sample ID"]) == SUBSET_STAAL], csor, procedures)
    schrijf(subset, os.path.join(UIT, f"{NAAM}.ttl"), kop + f"# Validatie-subset: staal {SUBSET_STAAL}.\n")

    n_obs = len(set(volledig.subjects(RDF.type, SOSA.Observation)))
    print(f"{len(rijen)} rijen -> {n_obs} observaties, "
          f"{len(set(volledig.subjects(RDF.type, SOSA.Sample)))} stalen, "
          f"{len(set(volledig.subjects(RDF.type, SOSA.Sampler)))} meetpunten; {len(volledig)} triples", file=sys.stderr)
    print(f"subset: {len(subset)} triples", file=sys.stderr)
    if ontbrekend:
        print(f"zonder CSOR-parameteraspect of -eenheid: {dict(ontbrekend)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
