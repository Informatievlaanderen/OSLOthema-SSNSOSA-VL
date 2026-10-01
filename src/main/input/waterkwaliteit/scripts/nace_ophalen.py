"""Haal een volledige Belgif-codelijst (bv. NACE-BEL 2025) recursief op.

Start van een lokaal ConceptScheme-bestand (zoals nacebel/nace2025.ttl), volgt
skos:hasTopConcept en daarna skos:narrower, en dereferencet elk concept als Turtle
op vocab.belgif.be. Enkel concepten binnen de namespace van het scheme worden gevolgd.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/nace_ophalen.py                                  # nacebel/nace2025.ttl
    python3 scripts/nace_ophalen.py nace2008.ttl                     # nacebel/nace2008.ttl
    python3 scripts/nace_ophalen.py nace2025.ttl -o uit.trig -w 4

Zonder argument wordt ../nacebel/nace2025.ttl t.o.v. dit script gebruikt. Een opgegeven
relatief pad wordt eerst t.o.v. de werkmap gezocht, en anders t.o.v. ../nacebel/.
De uitvoer komt standaard naast het invoerbestand.

Belgif publiceert dcterms:modified zonder seconden ("2026-08-24T14:50"^^xsd:dateTime), wat geen
geldige xsd:dateTime is. Het script vult de seconden aan (":00") in het invoerbestand zelf, omdat
de Maven-pipeline dat bestand valideert.

De uitvoer krijgt standaard de extensie .trig (Turtle-inhoud), zodat de Maven-pipeline,
die alle .ttl-bestanden onder src/main/input/ valideert, het grote bestand overslaat.

Vereist: rdflib.
"""
import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS

USER_AGENT = "OSLOthema-SSNSOSA-VL/nace_ophalen"
# xsd:dateTime zonder seconden, bv. "2026-08-24T14:50"^^xsd:dateTime
DATETIME_ZONDER_SECONDEN = re.compile(
    r'"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})((?:Z|[+-]\d{2}:\d{2})?)"\^\^'
    r'(xsd:dateTime|<http://www\.w3\.org/2001/XMLSchema#dateTime>)')
NACEBEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nacebel")


def zoek_invoer(pad):
    if os.path.isfile(pad):
        return os.path.abspath(pad)
    kandidaat = os.path.join(NACEBEL_DIR, pad)
    if os.path.isfile(kandidaat):
        return os.path.normpath(kandidaat)
    sys.exit(f"Invoerbestand niet gevonden: {pad} (ook niet in {os.path.normpath(NACEBEL_DIR)})")


def herstel_datetime(pad):
    """Vul in `pad` de seconden aan van xsd:dateTime-literals zonder seconden (in place)."""
    with open(pad, encoding="utf-8") as f:
        tekst = f.read()
    hersteld, n = DATETIME_ZONDER_SECONDEN.subn(r'"\1:00\2"^^\3', tekst)
    if n:
        with open(pad, "w", encoding="utf-8") as f:
            f.write(hersteld)
        print(f"{pad}: {n} xsd:dateTime zonder seconden aangevuld met :00", file=sys.stderr)


def haal_op(uri, pogingen=4):
    """Dereference `uri` als Turtle; geeft een rdflib Graph terug of werpt de laatste fout."""
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("invoer", nargs="?", default="nace2025.ttl", help="lokaal ConceptScheme-bestand")
    ap.add_argument("-o", "--uitvoer", help="uitvoerbestand (standaard <invoer>_volledig.trig)")
    ap.add_argument("-w", "--workers", type=int, default=8, help="aantal parallelle requests (standaard 8)")
    args = ap.parse_args()

    invoer = zoek_invoer(args.invoer)
    herstel_datetime(invoer)
    uitvoer = os.path.abspath(args.uitvoer or os.path.splitext(invoer)[0] + "_volledig.trig")
    os.makedirs(os.path.dirname(uitvoer), exist_ok=True)

    resultaat = Graph()
    resultaat.parse(invoer, format="turtle")
    for prefix, ns in resultaat.namespaces():
        resultaat.bind(prefix, ns)

    schemes = list(resultaat.subjects(RDF.type, SKOS.ConceptScheme))
    if not schemes:
        sys.exit(f"Geen skos:ConceptScheme gevonden in {invoer}")
    namespaces = [str(s).rstrip("/") + "/" for s in schemes]

    def binnen_scheme(o):
        return isinstance(o, URIRef) and any(str(o).startswith(ns) for ns in namespaces)

    gezien = set()
    grens = {o for s in schemes for o in resultaat.objects(s, SKOS.hasTopConcept) if binnen_scheme(o)}
    mislukt = []
    niveau = 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        while grens:
            niveau += 1
            gezien |= grens
            volgende = set()
            futures = {uri: pool.submit(haal_op, str(uri)) for uri in sorted(grens)}
            for uri, fut in futures.items():
                try:
                    g = fut.result()
                except Exception as e:  # noqa: BLE001 - rapporteer en ga verder
                    mislukt.append((str(uri), repr(e)))
                    continue
                resultaat += g
                volgende |= {o for o in g.objects(uri, SKOS.narrower) if binnen_scheme(o)}
            print(f"niveau {niveau}: {len(grens)} concepten opgehaald", file=sys.stderr)
            grens = volgende - gezien

    resultaat.serialize(destination=uitvoer, format="turtle")
    n_concepten = len(set(resultaat.subjects(RDF.type, SKOS.Concept)))
    print(f"{uitvoer}: {n_concepten} concepten, {len(resultaat)} triples", file=sys.stderr)
    if mislukt:
        print(f"{len(mislukt)} concepten konden niet opgehaald worden:", file=sys.stderr)
        for uri, fout in mislukt:
            print(f"  {uri}: {fout}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
