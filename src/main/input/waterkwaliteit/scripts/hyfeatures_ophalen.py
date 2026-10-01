"""Haal de OGC HY_Features-ontologie volledig op door recursief te dereferencen.

Start bij https://www.opengis.net/def/schema/hy_features/hyf (het scheme, owl:Ontology) en volgt elke
IRI binnen https://www.opengis.net/def/schema/hy_features/ die als subject of object voorkomt. Elke IRI
wordt als Turtle opgehaald (de OGC-definitieserver, Prez, levert per object een document).
Profielvarianten (?_profile=...), afbeeldingen en Prez-annotaties (https://prez.dev/) worden niet
overgenomen. owl:imports naar andere ontologieën wordt niet gevolgd.

Uitvoer: src/main/resources/net/opengis/www/def/schema/hy_features/hy_features.trig (Turtle-inhoud).
De extensie .trig houdt het bestand buiten de pipeline, die enkel .ttl inlaadt: de publicatie is
experimenteel, onvolledig als OWL (15 van de 34 feature types zijn enkel skos:Concept) en gebruikt
punning (dezelfde IRI als owl:Class én als skos:Concept). Ze dient als referentie, niet als
ingeladen ontologie (beslisdocument.md C3).

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/hyfeatures_ophalen.py [-w 8]

Vereist: rdflib.
"""
import argparse
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from rdflib import BNode, Graph, URIRef

HIER = os.path.dirname(os.path.abspath(__file__))
UIT = os.path.normpath(os.path.join(HIER, "..", "..", "..", "resources", "net", "opengis", "www", "def",
                                    "schema", "hy_features", "hy_features.trig"))
BASIS = "https://www.opengis.net/def/schema/hy_features/"
START = BASIS + "hyf"
PREZ = "https://prez.dev/"
USER_AGENT = "OSLOthema-SSNSOSA-VL/hyfeatures_ophalen"


def binnen(o):
    s = str(o)
    return isinstance(o, URIRef) and s.startswith(BASIS) and "?" not in s and not s.endswith((".png", ".svg"))


def haal_op(uri, pogingen=4):
    fout = None
    for poging in range(pogingen):
        try:
            req = urllib.request.Request(uri, headers={"Accept": "text/turtle", "User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            g = Graph()
            g.parse(data=data, format="turtle", publicID=uri)
            return g
        except (urllib.error.URLError, TimeoutError, ConnectionError, SyntaxError, ValueError) as e:
            fout = e
            time.sleep(2 ** poging)
    raise fout


def zonder_prez(g):
    """Verwijder Prez-annotaties: triples met een prez:-predicaat of -object, en de blank nodes die
    enkel daarvoor dienen ([] prez:currentProfile …)."""
    uit = Graph()
    for prefix, ns in g.namespaces():
        if not str(ns).startswith(PREZ):
            uit.bind(prefix, ns)
    for s, p, o in g:
        if str(p).startswith(PREZ) or str(o).startswith(PREZ) or str(s).startswith(PREZ):
            continue
        if isinstance(s, BNode) and any(str(p2).startswith(PREZ) for p2 in g.predicates(s, None)):
            continue
        uit.add((s, p, o))
    return uit


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-w", "--workers", type=int, default=8, help="aantal parallelle requests (standaard 8)")
    args = ap.parse_args()

    resultaat = Graph()
    resultaat.bind("hyf", BASIS + "hyf/")
    resultaat.bind("hyfeatures", BASIS)
    gezien, grens, mislukt, niveau = set(), {URIRef(START)}, [], 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while grens:
            niveau += 1
            gezien |= grens
            futures = {u: pool.submit(haal_op, str(u)) for u in sorted(grens)}
            volgende = set()
            for u, fut in futures.items():
                try:
                    g = zonder_prez(fut.result())
                except Exception as e:  # noqa: BLE001 - rapporteer en ga verder
                    mislukt.append((str(u), repr(e)))
                    continue
                for prefix, ns in g.namespaces():
                    resultaat.bind(prefix, ns, override=False)
                resultaat += g
                volgende |= {t for tr in g for t in (tr[0], tr[2]) if binnen(t)}
            print(f"niveau {niveau}: {len(grens)} IRI's opgehaald, {len(resultaat)} triples", file=sys.stderr)
            grens = volgende - gezien

    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    with open(UIT, "w", encoding="utf-8") as f:
        f.write("# OGC HY_Features (HydroFeature package), volledig gedereferenced van\n"
                f"# {START} (OGC-definitieserver) door scripts/hyfeatures_ophalen.py.\n"
                "# Niet manueel bewerken; opnieuw ophalen met het script.\n\n")
        f.write(resultaat.serialize(format="turtle"))
    print(f"{UIT}: {len(gezien)} IRI's, {len(resultaat)} triples", file=sys.stderr)
    if mislukt:
        print(f"{len(mislukt)} IRI's konden niet opgehaald worden:", file=sys.stderr)
        for u, fout in mislukt:
            print(f"  {u}: {fout}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
