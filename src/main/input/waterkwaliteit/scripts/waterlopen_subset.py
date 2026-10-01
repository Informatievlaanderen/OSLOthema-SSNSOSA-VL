"""Koppel de VMM-oppervlaktewatermeetplaatsen aan VHA-waterlopen en maak een validatie-subset.

Invoer:
- ../brondata_Jurgen/250114_Analyseresultaten_per_meetplaats_OW/SamplePoints.json
  (Sample Point, Lambert X/Y in EPSG:31370, Waterloop)
- ../waterlopen/wlas.trig en vhag.trig (herstelde versie, uitvoer van waterlopen_herstel.py)

Koppelregel per meetplaats (zie ../featureofinterest.md §3.3):
1. kandidaten = segmenten binnen ZOEKSTRAAL m van het punt;
2. kies het dichtstbijzijnde segment waarvan de roepnaam (code:naam) voorkomt in de
   VMM-waterloopnaam (hoofdletterongevoelig);
3. is er zo geen, dan het dichtstbijzijnde segment tout court;
4. `controle` = ja als er geen naamovereenkomst is of de afstand groter is dan DREMPEL m.

Uitvoer (in ../waterlopen):
- meetplaats_waterloop.csv: één rij per meetplaats met segment, waterloop, afstand, controle.
- waterlopen_meetplaatsen.ttl: alle triples van de gekoppelde segmenten en hun waterlopen, met hun
  geometrie (geo:hasGeometry naar een blank node, zie waterlopen_herstel.py stap 4).
  Die zijn klein genoeg voor de Maven-validatie (bewust .ttl).

Gebruik (vanuit om het even welke werkmap):
    uv run --with pyproj --with shapely python scripts/waterlopen_subset.py

Vereist: Apache Jena `riot`, pyproj, shapely.
"""
import csv
import json
import os
import re
import sys
import tempfile

from pyproj import Transformer
from shapely import wkt
from shapely.geometry import Point
from shapely.ops import transform
from shapely.strtree import STRtree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from waterlopen_herstel import CODE, NT, P_HASGEOMETRY, P_WKT, ntriples, schrijf_turtle  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
WATERLOPEN = os.path.normpath(os.path.join(HIER, "..", "waterlopen"))
SAMPLEPOINTS = os.path.normpath(os.path.join(
    HIER, "..", "brondata_Jurgen", "250114_Analyseresultaten_per_meetplaats_OW", "SamplePoints.json"))
ZOEKSTRAAL = 2000  # m
DREMPEL = 100  # m

P_NAAM = f"<{CODE}naam>"
P_VHAG = f"<{CODE}vhag>"
LIT = re.compile(r'^"(.*)"(?:@\w+|\^\^<[^>]*>)?$')


def literal(o):
    m = LIT.match(o)
    # riot schrijft N-Triples in UTF-8; enkel \" en \\ moeten ont-escaped worden
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\") if m else None


def lees_triples(pad, voorvoegsel):
    """Groepeer de N-Triples per subject: {subject: [(s, p, o), ...]}. Blank-node-labels krijgen
    `voorvoegsel`, zodat ze uniek blijven wanneer triples uit meerdere bestanden samengaan."""
    def bn(t):
        return f"_:{voorvoegsel}{t[2:]}" if t.startswith("_:") else t
    per_subject = {}
    for r in ntriples(pad):
        m = NT.match(r)
        if m:
            s, p, o = (bn(t) for t in m.groups())
            per_subject.setdefault(s, []).append((s, p, o))
    return per_subject


def met_geometrie(per_subject, s):
    """De triples van `s` plus die van zijn geometrie (blank node)."""
    triples = list(per_subject[s])
    for _, p, o in per_subject[s]:
        if p == P_HASGEOMETRY and o in per_subject:
            triples += per_subject[o]
    return triples


def wkt_van(per_subject, s):
    for _, p, o in met_geometrie(per_subject, s):
        if p == P_WKT:
            return o
    return None


def main():
    naar_l72 = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True).transform

    segmenten = lees_triples(os.path.join(WATERLOPEN, "wlas.trig"), "wlas")
    geoms, info = [], []
    for s, triples in segmenten.items():
        if s.startswith("_:"):
            continue
        d = {p: o for _, p, o in triples}
        w = wkt_van(segmenten, s)
        if w is None:
            continue
        geoms.append(transform(naar_l72, wkt.loads(literal(w))))
        info.append((s, literal(d.get(P_NAAM, "")) or "", d.get(P_VHAG)))
    boom = STRtree(geoms)
    print(f"{len(geoms)} segmenten ingelezen", file=sys.stderr)

    meetplaatsen = json.load(open(SAMPLEPOINTS, encoding="utf-8"))
    rijen, gekozen_seg, gekozen_wl = [], set(), set()
    for mp in meetplaatsen:
        punt = Point(mp["Lambert X"], mp["Lambert Y"])
        vmm_naam = (mp["Waterloop"] or "").upper()
        kandidaten = sorted(((punt.distance(geoms[i]), i) for i in boom.query(punt.buffer(ZOEKSTRAAL))))
        if not kandidaten:
            kandidaten = [(punt.distance(geoms[i]), i) for i in [boom.nearest(punt)]]
        met_naam = [(d, i) for d, i in kandidaten if info[i][1] and info[i][1].upper() in vmm_naam]
        afstand, i = (met_naam or kandidaten)[0]
        seg, seg_naam, wl = info[i]
        controle = "nee" if met_naam and afstand <= DREMPEL else "ja"
        rijen.append({
            "sample_point": mp["Sample Point"],
            "vmm_waterloop": mp["Waterloop"],
            "segment": seg.strip("<>"),
            "segment_naam": seg_naam,
            "waterloop": (wl or "").strip("<>"),
            "afstand_m": round(afstand, 1),
            "naamovereenkomst": "ja" if met_naam else "nee",
            "controle": controle,
        })
        gekozen_seg.add(seg)
        if wl:
            gekozen_wl.add(wl)

    csv_pad = os.path.join(WATERLOPEN, "meetplaats_waterloop.csv")
    with open(csv_pad, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rijen[0]))
        w.writeheader()
        w.writerows(rijen)

    waterlopen = lees_triples(os.path.join(WATERLOPEN, "vhag.trig"), "vhag")
    with tempfile.NamedTemporaryFile("w", suffix=".nt", delete=False, encoding="utf-8") as nt:
        for s in sorted(gekozen_seg):
            for t in met_geometrie(segmenten, s):
                nt.write(" ".join(t) + " .\n")
        ontbrekend = []
        for s in sorted(gekozen_wl):
            if s not in waterlopen:
                ontbrekend.append(s)
                continue
            for t in met_geometrie(waterlopen, s):
                nt.write(" ".join(t) + " .\n")
    ttl_pad = os.path.join(WATERLOPEN, "waterlopen_meetplaatsen.ttl")
    try:
        schrijf_turtle(nt.name, ttl_pad)
    finally:
        os.unlink(nt.name)

    n_controle = sum(r["controle"] == "ja" for r in rijen)
    print(f"{len(rijen)} meetplaatsen -> {len(gekozen_seg)} segmenten, {len(gekozen_wl)} waterlopen; "
          f"{n_controle} te controleren", file=sys.stderr)
    if ontbrekend:
        print(f"waterlopen niet in vhag: {ontbrekend}", file=sys.stderr)
    print(f"-> {csv_pad}\n-> {ttl_pad}", file=sys.stderr)


if __name__ == "__main__":
    main()
