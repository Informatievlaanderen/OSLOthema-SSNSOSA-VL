#!/usr/bin/env python3
"""Zet source/rapporterings_drempelwaarden.csv om naar twee bestanden:

- REGISTER: de codelijsten rapporteringscontext, rapporteringsgroep (met de te rapporteren
  parameteraspecten en de volgorde per context) en drempelwaardetype, als SKOS-conceptschema's.
  Ze staan in src/main/resources, zodat validate_file ze laadt en nagaat dat de drempelwaarden en
  toetsingen naar bestaande codes verwijzen (een klein register, zoals de CSOR-eenheden);
- DATA: drempelwaarden.ttl, elke rij met een drempel als csor:Drempelwaarde (een
  qudt:QuantityValue) met een geldigheidsperiode (dct:PeriodOfTime, dcat:startDate/endDate).

De termen van csor: staan als ontwerp in
src/main/resources/be/vlaanderen/omgeving/data/ns/csor/csor-rapportering.ttl.

Gebruik (vanuit src/main/input/drempelwaarden/):
    python3 scripts/drempelwaarden_to_rdf.py

Opschoning (zie README, Verbeterpunten):
- rijen zonder parameteraspect worden overgeslagen en gemeld;
- geldig-van-jaar 1900 en geldig-tot-jaar 2099 zijn plaatshouders voor "geen grens" en geven
  geen begin of einde;
- geldig-tot is inclusief in de bron, net als dcat:endDate.
"""
import csv
import sys
from collections import defaultdict
from decimal import Decimal

BRON = "source/rapporterings_drempelwaarden.csv"
DOEL = "drempelwaarden.ttl"
REGISTER = ("../../resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor/rapportering/"
            "rapportering.ttl")

ID = "https://data.omgeving.vlaanderen.be/id/"
SCHEMA = {
    "context": ID + "conceptscheme/csor/rapporteringscontext",
    "groep": ID + "conceptscheme/csor/rapporteringsgroep",
    "type": ID + "conceptscheme/csor/drempelwaardetype",
}
PLAATSHOUDER_VAN = "1900"
PLAATSHOUDER_TOT = "2099"


def iri(s):
    return f"<{s}>"


def lit(s, lang=None):
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"@{lang}' if lang else f'"{s}"'


def decimaal(s):
    t = format(Decimal(s).normalize(), "f")
    return t if "." in t else t + ".0"


def context_iri(code):
    return ID + "concept/csor/rapporteringscontext/" + code


def groep_iri(code):
    return ID + "concept/csor/rapporteringsgroep/" + code


def type_iri(code):
    return ID + "concept/csor/drempelwaardetype/" + code


def pas_iri(code):
    return ID + "concept/csor/parameteraspect/" + code


def eenheid_iri(code):
    return ID + "concept/csor/eenheid/" + code


def drempel_iri(r):
    # deterministische sleutel uit de bron (R10): groep, parameteraspect, type, geldig-van
    return (ID + "csor/drempelwaarde/" + r["rapporteringsgroep_code"] + "/" + r["parameter_aspect_code"]
            + "/" + r["drempelwaarde_type_code"] + "/" + r["drempel_geldig_van_jaar"])


def main():
    rijen = list(csv.DictReader(open(BRON, encoding="utf-8")))
    contexten, groepen, types, pas, eenheden = {}, {}, {}, {}, {}
    leden = defaultdict(set)
    volgorde = defaultdict(dict)
    drempels, overgeslagen = [], []

    for r in rijen:
        rc, rg = r["rapporteringscontext_code"], r["rapporteringsgroep_code"]
        contexten[rc] = r
        groepen[rg] = r
        volgorde[rc][int(r["rapporteringsgroep_volgnr_in_context"])] = rg
        if not r["parameter_aspect_code"]:
            overgeslagen.append(r)
            continue
        pas[r["parameter_aspect_code"]] = r
        leden[rg].add(r["parameter_aspect_code"])
        if r["drempelwaarde"]:
            types[r["drempelwaarde_type_code"]] = r
            eenheden[r["drempel_eenheid_code"]] = r
            drempels.append(r)

    reg = []
    w = reg.append
    w("# rapportering.ttl — GEGENEREERD door src/main/input/drempelwaarden/scripts/drempelwaarden_to_rdf.py")
    w("# uit src/main/input/drempelwaarden/source/rapporterings_drempelwaarden.csv. Niet met de hand wijzigen.")
    w("# ONTWERP: codelijsten rapporteringscontext, rapporteringsgroep en drempelwaardetype van het")
    w("# CSO-register, zoals voorgesteld in 'Ontwerp Codelijsten'; nog niet gepubliceerd.")
    w(f"# {len(contexten)} rapporteringscontexten, {len(groepen)} rapporteringsgroepen, "
      f"{len(types)} drempelwaardetypes.")
    w("")
    for p, n in [("csor", "https://data.omgeving.vlaanderen.be/ns/csor#"),
                 ("owl", "http://www.w3.org/2002/07/owl#"),
                 ("skos", "http://www.w3.org/2004/02/skos/core#")]:
        w(f"@prefix {p}: <{n}> .")
    w("")

    w("### CONCEPTSCHEMA'S")
    w("")
    for k, label in [("context", "Rapporteringscontexten"), ("groep", "Rapporteringsgroepen"),
                     ("type", "Drempelwaardetypes")]:
        w(f"{iri(SCHEMA[k])} a skos:ConceptScheme ;\n    skos:prefLabel {lit(label, 'nl')} .")
        w("")

    w("### RAPPORTERINGSCONTEXTEN")
    w("")
    for rc, r in sorted(contexten.items(), key=lambda x: int(x[0].split("_")[1])):
        w(f"{iri(context_iri(rc))} a csor:RapporteringsContext , skos:Concept ;")
        w(f"    skos:prefLabel {lit(r['rapporteringscontext_omschrijving'], 'nl')} ;")
        w(f"    skos:notation {lit(rc)} ;")
        w(f"    csor:symbool {lit(r['rapporteringscontext_symbool'])} ;")
        w(f"    owl:deprecated {'false' if r['rapporteringscontext_actief'] == 'true' else 'true'} ;")
        w(f"    skos:inScheme {iri(SCHEMA['context'])} ;")
        w(f"    skos:topConceptOf {iri(SCHEMA['context'])} .")
        w("")
        # volgorde van de groepen in de context
        lijst = " ".join(iri(groep_iri(volgorde[rc][n])) for n in sorted(volgorde[rc]))
        w(f"{iri(ID + 'collection/csor/rapporteringsgroep/' + rc)} a skos:OrderedCollection ;")
        w(f"    skos:prefLabel {lit('Rapporteringsgroepen ' + r['rapporteringscontext_omschrijving'], 'nl')} ;")
        w(f"    skos:memberList ( {lijst} ) .")
        w("")

    w("### RAPPORTERINGSGROEPEN")
    w("")
    for rg, r in sorted(groepen.items(), key=lambda x: int(x[0].split("_")[1])):
        w(f"{iri(groep_iri(rg))} a csor:RapporteringsGroep , skos:Concept ;")
        w(f"    skos:prefLabel {lit(r['rapporteringsgroep_omschrijving'], 'nl')} ;")
        if r["rapporteringsgroep_omschrijving_engels"]:
            w(f"    skos:prefLabel {lit(r['rapporteringsgroep_omschrijving_engels'], 'en')} ;")
        w(f"    skos:notation {lit(rg)} ;")
        w(f"    csor:symbool {lit(r['rapporteringsgroep_symbool'])} ;")
        w(f"    owl:deprecated {'false' if r['rapporteringsgroep_actief'] == 'true' else 'true'} ;")
        w(f"    csor:behoortTotRapporteringsContext {iri(context_iri(r['rapporteringscontext_code']))} ;")
        if leden[rg]:
            pl = " , ".join(iri(pas_iri(p)) for p in sorted(leden[rg], key=lambda x: int(x.split('_')[1])))
            w(f"    csor:teRapporterenParameterAspect {pl} ;")
        w(f"    skos:inScheme {iri(SCHEMA['groep'])} ;")
        w(f"    skos:topConceptOf {iri(SCHEMA['groep'])} .")
        w("")

    w("### DREMPELWAARDETYPES")
    w("")
    for t, r in sorted(types.items(), key=lambda x: int(x[0].split("_")[1])):
        w(f"{iri(type_iri(t))} a csor:DrempelwaardeType , skos:Concept ;")
        w(f"    skos:prefLabel {lit(r['drempelwaarde_type_omschrijving'], 'nl')} ;")
        w(f"    skos:notation {lit(t)} ;")
        w(f"    skos:inScheme {iri(SCHEMA['type'])} ;")
        w(f"    skos:topConceptOf {iri(SCHEMA['type'])} .")
        w("")

    out = []
    w = out.append
    w("# drempelwaarden.ttl — GEGENEREERD door scripts/drempelwaarden_to_rdf.py uit")
    w("# source/rapporterings_drempelwaarden.csv. Niet met de hand wijzigen.")
    w(f"# {len(drempels)} drempelwaarden; {len(overgeslagen)} rijen zonder parameteraspect overgeslagen.")
    w("# De codelijsten staan in src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor/")
    w("# rapportering/rapportering.ttl.")
    w("")
    for p, n in [("csor", "https://data.omgeving.vlaanderen.be/ns/csor#"),
                 ("dcat", "http://www.w3.org/ns/dcat#"),
                 ("dct", "http://purl.org/dc/terms/"),
                 ("qudt", "http://qudt.org/schema/qudt/"),
                 ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
                 ("xsd", "http://www.w3.org/2001/XMLSchema#")]:
        w(f"@prefix {p}: <{n}> .")
    w("")
    w("### DREMPELWAARDEN")
    w("# Waarde met eenheid (R3); geldigheid in jaren, einde inclusief (dcat:endDate).")
    w("")
    for r in sorted(drempels, key=lambda r: (int(r["rapporteringsgroep_code"].split("_")[1]),
                                             int(r["parameter_aspect_code"].split("_")[1]),
                                             r["drempelwaarde_type_code"], r["drempel_geldig_van_jaar"])):
        d = drempel_iri(r)
        van, tot = r["drempel_geldig_van_jaar"], r["drempel_geldig_tot_jaar"]
        periode = f"vanaf {van}" if van != PLAATSHOUDER_VAN else "zonder begin"
        if tot and tot != PLAATSHOUDER_TOT:
            periode += f" tot en met {tot}"
        label = (f"{r['rapporteringscontext_omschrijving']}, {r['parameter_omschrijving']} "
                 f"({r['parameter_aspect_omschrijving']}), {r['drempelwaarde_type_omschrijving'].lower()}, "
                 f"{periode}: {decimaal(r['drempelwaarde'])} {r['drempel_eenheid_symbool']}")
        w(f"{iri(d)} a csor:Drempelwaarde , qudt:QuantityValue ;")
        w(f"    rdfs:label {lit(label, 'nl')} ;")
        w(f"    csor:behoortTotRapporteringsGroep {iri(groep_iri(r['rapporteringsgroep_code']))} ;")
        w(f"    csor:voorParameterAspect {iri(pas_iri(r['parameter_aspect_code']))} ;")
        w(f"    csor:heeftDrempelwaardeType {iri(type_iri(r['drempelwaarde_type_code']))} ;")
        w(f"    qudt:numericValue {decimaal(r['drempelwaarde'])} ;")
        w(f"    qudt:hasUnit {iri(eenheid_iri(r['drempel_eenheid_code']))} ;")
        w(f"    dct:temporal {iri(d + '/geldigheid')} .")
        w("")
        delen = []
        if van != PLAATSHOUDER_VAN:
            delen.append(f'    dcat:startDate "{van}"^^xsd:gYear')
        if tot and tot != PLAATSHOUDER_TOT:
            delen.append(f'    dcat:endDate "{tot}"^^xsd:gYear')
        w(f"{iri(d + '/geldigheid')} a dct:PeriodOfTime"
          + (" ;\n" + " ;\n".join(delen) if delen else "") + " .")
        w("")

    w("### VERWEZEN REGISTERCONCEPTEN")
    w("# Enkel getypeerd, zodat de SHACL-shapes ze herkennen (qudt:hasUnit vraagt een qudt:Unit, R3;")
    w("# csor:voorParameterAspect een csor:ParameterAspect). Labels, definities en de mapping naar")
    w("# QUDT staan in het CSO-register.")
    w("")
    for e in sorted(eenheden, key=lambda x: int(x.split("_")[1])):
        w(f"{iri(eenheid_iri(e))} a csor:Eenheid , qudt:Unit .")
    for p in sorted({r["parameter_aspect_code"] for r in drempels}, key=lambda x: int(x.split("_")[1])):
        w(f"{iri(pas_iri(p))} a csor:ParameterAspect .")
    w("")

    with open(DOEL, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    import os
    os.makedirs(os.path.dirname(REGISTER), exist_ok=True)
    with open(REGISTER, "w", encoding="utf-8") as f:
        f.write("\n".join(reg))
    print(f"{DOEL}: {len(contexten)} contexten, {len(groepen)} groepen, {len(types)} types, "
          f"{len(drempels)} drempelwaarden, {len(pas)} parameteraspecten", file=sys.stderr)
    for r in overgeslagen:
        print(f"  overgeslagen (geen parameteraspect): {r['rapporteringscontext_symbool']} "
              f"{r['rapporteringsgroep_symbool']} {r['parameter_omschrijving']}", file=sys.stderr)


if __name__ == "__main__":
    main()
