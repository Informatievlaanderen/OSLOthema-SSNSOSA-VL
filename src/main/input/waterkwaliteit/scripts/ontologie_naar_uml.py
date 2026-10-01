"""Genereer een UML-klassendiagram (Mermaid classDiagram) uit de waterkwaliteit-ontologie.

Invoer: src/main/resources/be/vlaanderen/data/ns/waterkwaliteit/waterkwaliteit.ttl
Uitvoer: ../waterkwaliteit_uml.mmd

Wat in het diagram komt:
- klassen: elke owl:Class die waterkwaliteit.ttl declareert (wk, en de gebruikte CSOR- en
  VHA-klassen), plus hun benoemde superklassen (SOSA, PROV, GeoSPARQL) als externe klassen;
- overerving: rdfs:subClassOf naar een benoemde klasse;
- eigenschappen: de OWL-restricties van een klasse, per property samengevoegd zoals
  OwlToShaclGenerator dat doet (someValuesFrom = minstens 1, tenzij een owl:minCardinality 0 op
  dezelfde property; maxCardinality = maximum; unionOf = keuze). Een eigenschap naar een klasse
  in het diagram wordt een associatie, alle andere worden attributen.

Het diagram toont dus precies wat de gegenereerde SHACL afdwingt, niet de restricties die enkel in
geïmporteerde ontologieën (csor.ttl, waterlopen.ttl) staan.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/ontologie_naar_uml.py
    mmdc -i waterkwaliteit_uml.mmd -o waterkwaliteit_uml.svg     # Mermaid CLI

Vereist: rdflib.
"""
import os
import sys

from rdflib import BNode, Graph, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF, RDFS

HIER = os.path.dirname(os.path.abspath(__file__))
ONTOLOGIE = os.path.normpath(os.path.join(
    HIER, "..", "..", "..", "resources", "be", "vlaanderen", "data", "ns", "waterkwaliteit", "waterkwaliteit.ttl"))
UIT = os.path.normpath(os.path.join(HIER, "..", "waterkwaliteit_uml.mmd"))
# Een keuze (owl:unionOf) tussen klassen wordt een associatie per klasse, met de UML-beperking {or}
# en per pijl 0..*; de multipliciteit van de restrictie geldt voor de keuze samen.

PREFIXEN = {
    "https://data.vlaanderen.be/ns/waterkwaliteit#": "wk",
    "https://data.omgeving.vlaanderen.be/ns/csor#": "csor",
    "https://data.omgeving.vlaanderen.be/ns/waterlopen#": "waterlopen",
    "http://www.w3.org/ns/sosa/": "sosa",
    "http://www.w3.org/ns/prov#": "prov",
    "http://www.opengis.net/ont/geosparql#": "geo",
    "http://www.w3.org/2006/time#": "time",
    "http://qudt.org/schema/qudt/": "qudt",
    "http://purl.org/dc/terms/": "dct",
    "http://www.w3.org/ns/adms#": "adms",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
}
# Kleur per namespace (kleurpalet uit CLAUDE.md §6)
STIJL = {
    "wk": "fill:#e54b89,stroke:#2E5C8A,color:#fff",
    "csor": "fill:#fe7130,stroke:#2E5C8A,color:#000",
    "waterlopen": "fill:#60c4e4,stroke:#2E5C8A,color:#000",
    "extern": "fill:#eeeeee,stroke:#2E5C8A,color:#000",
}


def qname(uri):
    for ns, p in PREFIXEN.items():
        if str(uri).startswith(ns):
            return f"{p}:{str(uri)[len(ns):]}"
    return str(uri)


def mid(uri):
    """Mermaid-id: enkel letters, cijfers en _."""
    return qname(uri).replace(":", "_").replace("-", "_")


def getal(g, r, p):
    v = g.value(r, p)
    return int(v) if v is not None else None


def bereik(g, r):
    """Lijst van bereikklassen van een restrictie, en of het een keuze (unionOf) is."""
    v = g.value(r, OWL.someValuesFrom) or g.value(r, OWL.allValuesFrom)
    if v is None:
        return [], False
    if isinstance(v, BNode) and g.value(v, OWL.unionOf) is not None:
        return [m for m in Collection(g, g.value(v, OWL.unionOf)) if isinstance(m, URIRef)], True
    return ([v] if isinstance(v, URIRef) else []), False


def is_subklasse(g, sub, sup):
    """sub rdfs:subClassOf* sup volgens de ontologie."""
    return sup in g.transitive_objects(sub, RDFS.subClassOf)


def eigenschappen(g, cls):
    """{property: (bereik, keuze, min, max)}, samengevoegd per property."""
    per_prop = {}
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and isinstance(g.value(r, OWL.onProperty), URIRef):
            per_prop.setdefault(g.value(r, OWL.onProperty), []).append(r)
    uit = {}
    for prop, rs in sorted(per_prop.items(), key=lambda kv: qname(kv[0])):
        versoepeld = any(getal(g, r, OWL.minCardinality) == 0 for r in rs)
        mins, maxs, enkel, keuze = [], [], [], []
        for r in rs:
            k = getal(g, r, OWL.cardinality)
            m = k if k is not None else getal(g, r, OWL.minCardinality)
            if m is None and (r, OWL.someValuesFrom, None) in g and not versoepeld:
                m = 1
            if m:
                mins.append(m)
            x = k if k is not None else getal(g, r, OWL.maxCardinality)
            if x is not None:
                maxs.append(x)
            b, is_keuze = bereik(g, r)
            (keuze if is_keuze else enkel).extend(b)
        # de meest specifieke beperking: een keuze (unionOf) gaat voor een enkelvoudig bereik, en van
        # meerdere enkelvoudige bereiken blijven enkel die zonder subklasse in de lijst
        b = keuze or list(dict.fromkeys(enkel))
        if not keuze:
            b = [x for x in b if not any(y != x and is_subklasse(g, y, x) for y in b)]
        uit[prop] = (b, bool(keuze), max(mins) if mins else 0, min(maxs) if maxs else None)
    return uit


def multipliciteit(lo, hi):
    if hi is None:
        return f"{lo}..*"
    return str(lo) if lo == hi else f"{lo}..{hi}"


def main():
    g = Graph().parse(ONTOLOGIE, format="turtle")
    eigen = sorted({c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)}, key=qname)
    supers = {(c, s) for c in eigen for s in g.objects(c, RDFS.subClassOf) if isinstance(s, URIRef)}
    klassen = set(eigen) | {s for _, s in supers}

    regels = ["%% Gegenereerd door scripts/ontologie_naar_uml.py uit waterkwaliteit.ttl; niet manueel bewerken.",
              "classDiagram", "    direction TB", ""]
    associaties = []
    for c in sorted(klassen, key=qname):
        attr = []
        if c in eigen:
            for prop, (b, keuze, lo, hi) in eigenschappen(g, c).items():
                mult = multipliciteit(lo, hi)
                if b and all(x in klassen for x in b):
                    naam = qname(prop).split(":", 1)[1]
                    if keuze:
                        # keuze tussen klassen: per pijl 0..*, samen de multipliciteit (UML {or})
                        naam = f"{naam} {{or}} {mult}"
                        mult = f"0..{'*' if hi is None else hi}"
                    for x in b:
                        # label zonder prefix: Mermaid aanvaardt geen ':' in een associatielabel (CLAUDE.md §6)
                        associaties.append(f'    {mid(c)} --> "{mult}" {mid(x)} : {naam}')
                else:
                    typ = " | ".join(qname(x) for x in b) or "?"
                    attr.append(f"        +{qname(prop)} : {typ} [{mult}]")
        regels.append(f'    class {mid(c)}["{qname(c)}"] {{')
        if c not in eigen:
            regels.append("        <<extern>>")
        regels += attr
        regels.append("    }")
    regels.append("")
    for c, s in sorted(supers, key=lambda t: (qname(t[0]), qname(t[1]))):
        regels.append(f"    {mid(s)} <|-- {mid(c)}")
    regels.append("")
    regels += associaties
    regels.append("")
    for c in sorted(klassen, key=qname):
        p = qname(c).split(":")[0]
        regels.append(f"    style {mid(c)} {STIJL.get(p if c in eigen else 'extern', STIJL['extern'])}")

    with open(UIT, "w", encoding="utf-8") as f:
        f.write("\n".join(regels) + "\n")
    print(f"{UIT}: {len(eigen)} klassen uit de ontologie, {len(klassen) - len(eigen)} externe superklassen, "
          f"{len(supers)} overervingen, {len(associaties)} associaties", file=sys.stderr)


if __name__ == "__main__":
    main()
