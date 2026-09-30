"""Herstel de IRI-fout in de VHA-waterlopen-LOD (shapefile_to_rdf).

Probleem: een VHA-waterloop (code:Vhag) krijgt als IRI zijn objectnummer
(waterloop:<oidn>), terwijl segmenten, categorietrajecten én de waterloop zelf via code:vhag
naar de gewestcode verwijzen (waterloop:<vhag>). Die verwijzingen komen daardoor bij een
andere waterloop uit of bij niets. Zie ../featureofinterest.md §3.4.

Herstel:
1. vhag: subject waterloop:<oidn> -> waterloop:<vhag>. De zelfverwijzing `code:vhag` wordt
   `skos:notation "<vhag>"^^code:vhag`, en het oude nummer blijft bewaard als
   `skos:notation "<oidn>"^^code:oidn`.
2. wlas: code:vhazonenr krijgt een eigen namespace
   (…/id/waterloop/vhazone/<nr>) in plaats van waterloop:<nr>.
3. wlas en vhacattraj: code:vhag verwijst al naar de gewestcode en blijft ongewijzigd.

Invoer: de originele vhag, wlas en vhacattraj (.ttl of .trig), standaard uit
~/git/shapefile_to_rdf/rdf. Al herstelde bestanden worden geweigerd.
Uitvoer: <naam>.trig (Turtle-inhoud) in ../waterlopen, buiten de Maven-validatie.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/waterlopen_herstel.py                    # ~/git/shapefile_to_rdf/rdf -> ../waterlopen
    python3 scripts/waterlopen_herstel.py -i <bronmap> -o <uitvoermap>

Vereist: Apache Jena `riot` op het PATH (streaming naar N-Triples en terug naar Turtle).
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
WATERLOOP = "https://data.omgeving.vlaanderen.be/id/waterloop/"
VHAZONE = "https://data.omgeving.vlaanderen.be/id/waterloop/vhazone/"
CODE = "https://data.omgeving.vlaanderen.be/ns/waterlopen#"
SKOS_NOTATION = "<http://www.w3.org/2004/02/skos/core#notation>"
RDF_TYPE = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
P_VHAG = f"<{CODE}vhag>"
P_VHAZONENR = f"<{CODE}vhazonenr>"

PREFIXEN = f"""@prefix code: <{CODE}> .
@prefix waterloop: <{WATERLOOP}> .
@prefix vhazone: <{VHAZONE}> .
@prefix waterloopsegment: <{WATERLOOP}waterloopsegment/> .
@prefix categorietraject: <{WATERLOOP}categorietraject/> .
@prefix categorie: <https://data.omgeving.vlaanderen.be/id/concept/waterlopen/categorie/> .
@prefix beheerder: <https://data.omgeving.vlaanderen.be/id/concept/waterlopen/beheerder/> .
@prefix bekken: <https://data.omgeving.vlaanderen.be/id/concept/waterlopen/bekken/> .
@prefix waterlichaam: <https://data.omgeving.vlaanderen.be/id/concept/waterlopen/waterlichaam/> .
@prefix stroomgebied: <https://data.omgeving.vlaanderen.be/id/concept/waterlopen/stroomgebied/> .
@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xs: <http://www.w3.org/2001/XMLSchema#> .
"""

# N-Triples-regel: <s> <p> o .   (o = IRI of literal)
NT = re.compile(r"^(<[^>]*>) (<[^>]*>) (.*) \.$")


def zoek(invoermap, naam):
    for ext in (".trig", ".ttl"):
        pad = os.path.join(invoermap, naam + ext)
        if os.path.isfile(pad):
            return pad
    sys.exit(f"{naam}.trig of {naam}.ttl niet gevonden in {invoermap}")


def ntriples(pad):
    """Stream een Turtle/TriG-bestand als N-Triples-regels via riot."""
    # Voor .trig: N-Quads als uitvoer (vermijdt de riot-waarschuwing). Triples in de standaardgraaf
    # zijn dan identieke N-Triples-regels; triples in een benoemde graaf matchen NT niet en stoppen het script.
    syntax, uitvoer = ("trig", "nquads") if pad.endswith(".trig") else ("turtle", "nt")
    proc = subprocess.Popen(["riot", f"--syntax={syntax}", f"--output={uitvoer}", pad],
                            stdout=subprocess.PIPE, text=True, encoding="utf-8")
    for regel in proc.stdout:
        regel = regel.rstrip("\n")
        if regel:
            yield regel
    if proc.wait() != 0:
        sys.exit(f"riot faalde op {pad}")


def schrijf_turtle(nt_pad, uit_pad):
    """Zet een N-Triples-bestand om naar leesbare Turtle met prefixen (inhoud geldig als TriG)."""
    with tempfile.NamedTemporaryFile("w", suffix=".ttl", delete=False, encoding="utf-8") as tmp:
        tmp.write(PREFIXEN)
        with open(nt_pad, encoding="utf-8") as f:
            for regel in f:
                tmp.write(regel)
    try:
        with open(uit_pad, "w", encoding="utf-8") as uit:
            subprocess.run(["riot", "--syntax=turtle", "--formatted=turtle", tmp.name], stdout=uit, check=True)
    finally:
        os.unlink(tmp.name)


def herstel_vhag(pad, werkmap):
    """Geeft (pad naar herstelde N-Triples, set van geldige waterloop-IRI's)."""
    regels = list(ntriples(pad))
    nieuw = {}  # oude subject-IRI -> nieuwe IRI
    for r in regels:
        m = NT.match(r)
        if m and m.group(2) == P_VHAG:
            nieuw[m.group(1)] = m.group(3)
    if not nieuw:
        sys.exit(f"{pad}: geen code:vhag-zelfverwijzingen gevonden; dit bestand lijkt al hersteld")
    if len(set(nieuw.values())) != len(nieuw):
        sys.exit("vhag-codes zijn niet uniek: herstel afgebroken")
    uit = os.path.join(werkmap, "vhag.nt")
    with open(uit, "w", encoding="utf-8") as f:
        for r in regels:
            m = NT.match(r)
            if not m:
                sys.exit(f"onverwachte N-Triples-regel: {r[:120]}")
            s, p, o = m.groups()
            ns = nieuw.get(s, s)
            if p == P_VHAG:
                code = o[len("<" + WATERLOOP):-1]
                oidn = s[len("<" + WATERLOOP):-1]
                f.write(f'{ns} {SKOS_NOTATION} "{code}"^^<{CODE}vhag> .\n')
                f.write(f'{ns} {SKOS_NOTATION} "{oidn}"^^<{CODE}oidn> .\n')
            else:
                f.write(f"{ns} {p} {o} .\n")
    print(f"vhag: {len(nieuw)} waterlopen hernoemd naar hun gewestcode", file=sys.stderr)
    return uit, set(nieuw.values())


def herstel_verwijzers(pad, naam, werkmap, geldig):
    uit = os.path.join(werkmap, f"{naam}.nt")
    refs, dangling, zones = set(), set(), 0
    with open(uit, "w", encoding="utf-8") as f:
        for r in ntriples(pad):
            m = NT.match(r)
            if not m:
                sys.exit(f"onverwachte N-Triples-regel: {r[:120]}")
            s, p, o = m.groups()
            if p == P_VHAG:
                refs.add(o)
                if o not in geldig:
                    dangling.add(o)
            elif p == P_VHAZONENR and o.startswith("<" + WATERLOOP):
                o = "<" + VHAZONE + o[len("<" + WATERLOOP):]
                zones += 1
            f.write(f"{s} {p} {o} .\n")
    print(f"{naam}: {len(refs)} verschillende code:vhag-verwijzingen, {len(dangling)} zonder waterloop in vhag"
          + (f"; {zones} vhazonenr verplaatst naar {VHAZONE}" if zones else ""), file=sys.stderr)
    return uit, dangling


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--invoer", default="~/git/shapefile_to_rdf/rdf", help="map met de originele vhag/wlas/vhacattraj")
    ap.add_argument("-o", "--uitvoer", default=os.path.join(HIER, "..", "waterlopen"), help="uitvoermap (standaard ../waterlopen)")
    args = ap.parse_args()
    invoer = os.path.normpath(os.path.expanduser(args.invoer))
    uitvoer = os.path.normpath(os.path.expanduser(args.uitvoer))
    if uitvoer == invoer:
        sys.exit("uitvoermap = invoermap: dat zou de originelen overschrijven")
    os.makedirs(uitvoer, exist_ok=True)

    with tempfile.TemporaryDirectory() as werk:
        vhag_nt, geldig = herstel_vhag(zoek(invoer, "vhag"), werk)
        resultaten = [("vhag", vhag_nt)]
        for naam in ("wlas", "vhacattraj"):
            nt, dangling = herstel_verwijzers(zoek(invoer, naam), naam, werk, geldig)
            resultaten.append((naam, nt))
            if dangling:
                print(f"  vb. zonder waterloop: {sorted(dangling)[:5]}", file=sys.stderr)
        for naam, nt in resultaten:
            doel = os.path.join(uitvoer, f"{naam}.trig")
            schrijf_turtle(nt, doel)
            print(f"-> {doel}", file=sys.stderr)


if __name__ == "__main__":
    main()
