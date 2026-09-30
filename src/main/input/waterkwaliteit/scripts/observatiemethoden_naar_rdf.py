"""Zet de VITO-lijst observatiemethoden om naar RDF (TriG-bestand met Turtle-inhoud).

Invoer:  ../brondata_Jurgen/Lijst_observatiemethodes_VITO-v1/Observatiemethoden.json
         (JSON-omzetting van de tab `Observatiemethoden`, zie brondata_Jurgen/xlsx_naar_json.py)
Uitvoer: ../brondata_Jurgen/Lijst_observatiemethodes_VITO-v1/rdf_transformed/observatiemethoden.trig

Per record (hoofdprocedure of jaarversie):
    <URI> a sosa:Procedure, skos:Concept ;
        skos:prefLabel     Pref_label@nl ;
        skos:notation      Notation ;
        skos:inScheme      <…/conceptscheme/observatieprocedure> ;
        dct:isVersionOf    <Is versie van>       (enkel jaarversies)
        dct:issued         "Jaar"^^xsd:gYear     (enkel jaarversies)
        skos:definition    Definition@nl          (enkel indien ingevuld)
        prov:hadPrimarySource <pdf-bestand>       (enkel indien ingevuld)

`owl:isVersionOf` bestaat niet in OWL; `dct:isVersionOf` is de gangbare property.
Lege velden leveren geen triple op.
Het jaar van een versie staat als `dct:issued` met datatype xsd:gYear (XML Schema kent geen
"xs:year").

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/observatiemethoden_naar_rdf.py

Vereist: rdflib.
"""
import json
import os
import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, PROV, RDF, SKOS, XSD

HIER = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.normpath(os.path.join(HIER, "..", "brondata_Jurgen", "Lijst_observatiemethodes_VITO-v1"))
BRON = os.path.join(MAP, "Observatiemethoden.json")
UIT = os.path.join(MAP, "rdf_transformed", "observatiemethoden.trig")

SOSA = Namespace("http://www.w3.org/ns/sosa/")
OBSPROC = Namespace("https://data.omgeving.vlaanderen.be/id/concept/observatieprocedure/")
SCHEMA = URIRef("https://data.omgeving.vlaanderen.be/id/conceptscheme/observatieprocedure")


def gevuld(v):
    return v is not None and str(v).strip() != ""


def main():
    rijen = json.load(open(BRON, encoding="utf-8"))
    g = Graph()
    for p, ns in (("sosa", SOSA), ("skos", SKOS), ("dct", DCTERMS), ("prov", PROV),
                  ("procedure", OBSPROC), ("xsd", XSD)):
        g.bind(p, ns)
    g.add((SCHEMA, RDF.type, SKOS.ConceptScheme))

    for r in rijen:
        s = URIRef(r["URI"])
        g.add((s, RDF.type, SOSA.Procedure))
        g.add((s, RDF.type, SKOS.Concept))
        g.add((s, SKOS.prefLabel, Literal(r["Pref_label"], lang="nl")))
        g.add((s, SKOS.notation, Literal(r["Notation"])))
        g.add((s, SKOS.inScheme, SCHEMA))
        if gevuld(r["Is versie van"]):
            g.add((s, DCTERMS.isVersionOf, URIRef(r["Is versie van"])))
        if gevuld(r["Jaar"]):
            g.add((s, DCTERMS.issued, Literal(f"{int(r['Jaar']):04d}", datatype=XSD.gYear)))
        if gevuld(r["Definition"]):
            g.add((s, SKOS.definition, Literal(r["Definition"], lang="nl")))
        if gevuld(r["pdf-bestand"]):
            g.add((s, PROV.hadPrimarySource, URIRef(r["pdf-bestand"])))

    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    kop = ("# Observatiemethoden (voorstel VITO, v1) als sosa:Procedure + skos:Concept\n"
           "# Gegenereerd door scripts/observatiemethoden_naar_rdf.py uit Observatiemethoden.json;\n"
           "# niet manueel bewerken.\n")
    with open(UIT, "w", encoding="utf-8") as f:
        f.write(kop + g.serialize(format="turtle"))
    versies = len(set(g.subjects(DCTERMS.isVersionOf, None)))
    print(f"{len(rijen)} records -> {len(g)} triples ({len(rijen) - versies} hoofdprocedures, "
          f"{versies} jaarversies) -> {UIT}", file=sys.stderr)


if __name__ == "__main__":
    main()
