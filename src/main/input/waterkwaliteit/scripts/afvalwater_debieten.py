"""Stap 3 van stappenplan.md: jaardebieten van lozingen (250129) naar SSN/SOSA 2023.

Invoer:
- ../brondata_Jurgen/250129_AW_Lozingsdebieten_2023_geleverd/Pagina2.json
- CSOR-codelijsten in ~/git/csor (via waterkwaliteit_gemeen.Csor)
- optioneel het RIE-IEPR-datavoorbeeld (--riepr) om meetputten aan RIE-IEPR-meetpunten te koppelen
  via vmm:lozingspuntCode

Uitvoer (../nieuw_model/afvalwater_debieten/):
- afvalwater_debieten.trig  alle 1555 jaardebieten (Turtle-inhoud, buiten de Maven-validatie)
- afvalwater_debieten.ttl   AGC Glass Mol (meetputten SUBSET_MEETPUTTEN) als validatie-subset

Model (zie bespreking.md in de uitvoermap):
  lozing (FOI) <-hasFeatureOfInterest- observatie jaardebiet -hasResult-> resultaat (m³/jr)
  observatie -observedProperty-> CSOR "Q (standaard in water): debiet"; -prov:atLocation-> meetput;
             -prov:used-> databron (IMJV of MNT)
  collectie "jaardebieten <jaar>": gedeelde observedProperty en fenomeentijd (time:Interval, R12)

Dezelfde ex:-namespace als stap 1 (afvalwater_concentraties): meetput, lozing en exploitatie
krijgen dezelfde IRI's en dezelfde triples, zodat beide voorbeelden samenvoegbaar zijn. De
meetput krijgt hier geen geometrie (die staat in stap 1; de bronnen verschillen < 1 m).

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/afvalwater_debieten.py [--csor ~/git/csor] [--riepr <agc-glass_MJV_…ttl>]

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
from waterkwaliteit_gemeen import ADMS, QUDT, SOSA, TIME, Csor, decimaal  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.normpath(os.path.join(
    HIER, "..", "brondata_Jurgen", "250129_AW_Lozingsdebieten_2023_geleverd", "Pagina2.json"))
UIT = os.path.normpath(os.path.join(HIER, "..", "nieuw_model", "afvalwater_debieten"))
NAAM = "afvalwater_debieten"
SUBSET_MEETPUTTEN = {"2400006", "2400007"}  # AGC Glass Europe vestiging Mol en AGC Fabrication - Kempenglas
RIEPR_VOORBEELD = "~/git/RIE-IEPR/documentatie/datamodel/datavoorbeelden/agc-glass_MJV_18-09-2026.ttl"

EX = Namespace("https://example.org/waterkwaliteit/afvalwater/")   # zelfde namespace als stap 1
KOLOM_DEBIET = "Jaardebiet (m³/jaar) (IMJV --> MNT)"
EENHEID_BRON = {"m³/jaar": "m³/jr"}  # bronnotatie -> CSOR-symbool
DATABRONNEN = {
    "IMJV": ("Integraal milieujaarverslag (IMJV)", None),
    "MNT": ("MNT", "Betekenis van de afkorting te bevestigen door de VMM (stappenplan.md V9)."),
}


def riepr_meetpunten(pad):
    """VMM-meetputnummer -> (niet-geversioneerde) RIE-IEPR-meetpunt-IRI, via vmm:lozingspuntCode."""
    pad = os.path.expanduser(pad)
    if not os.path.isfile(pad):
        return {}
    g = Graph()
    g.parse(pad)
    uit = {}
    for s, ident in g.subject_objects(ADMS.identifier):
        for n in g.objects(ident, SKOS.notation):
            if str(getattr(n, "datatype", "") or "").endswith("lozingspuntCode"):
                uit[str(n)] = g.value(s, DCTERMS.isVersionOf) or s
    return uit


def bouw(rijen, csor, riepr):
    g = Graph()
    for p, ns in (("ex", EX), ("sosa", SOSA), ("qudt", QUDT), ("time", TIME), ("adms", ADMS), ("prov", PROV),
                  ("dct", DCTERMS), ("skos", SKOS), ("xsd", XSD), ("rdfs", RDFS),
                  ("csor-parameteraspect", "https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/"),
                  ("csor-eenheid", "https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/"),
                  ("riepr-meetpunt", "https://data.mjv.omgeving.vlaanderen.be/id/meetpunt/")):
        g.bind(p, ns)

    vmm = EX["organisatie-vmm"]
    g.add((vmm, RDF.type, PROV.Organization))
    g.add((vmm, RDFS.label, Literal("Vlaamse Milieumaatschappij", lang="nl")))
    for code, (label, opmerking) in DATABRONNEN.items():
        bron = EX[f"databron-{code}"]
        g.add((bron, RDF.type, PROV.Entity))
        g.add((bron, RDFS.label, Literal(label, lang="nl")))
        if opmerking:
            g.add((bron, RDFS.comment, Literal(opmerking, lang="nl")))

    pa, eenheid = csor.parameteraspect_symbool("Q", "water", EENHEID_BRON["m³/jaar"])
    if pa is None or eenheid is None:
        sys.exit("geen eenduidig CSOR-parameteraspect voor Q (standaard in water) in m³/jr")
    g.add((pa, RDF.type, SOSA.Property))
    g.add((pa, RDFS.label, Literal(str(csor.label(pa)), lang="nl")))
    g.add((eenheid, RDFS.label, Literal(str(csor.label(eenheid)), lang="nl")))

    for jaar in sorted({r["Jaar"] for r in rijen}):
        periode = EX[f"periode-{jaar}"]
        begin, einde = EX[f"tijdstip-{jaar}-01-01T000000"], EX[f"tijdstip-{jaar + 1}-01-01T000000"]
        g.add((periode, RDF.type, TIME.Interval))
        g.add((periode, TIME.hasBeginning, begin))
        g.add((periode, TIME.hasEnd, einde))           # half-open interval (R12): einde exclusief
        for t, j in ((begin, jaar), (einde, jaar + 1)):
            g.add((t, RDF.type, TIME.Instant))
            g.add((t, TIME.inXSDDateTime, Literal(f"{j}-01-01T00:00:00", datatype=XSD.dateTime)))
        collectie = EX[f"collectie-jaardebieten-{jaar}"]
        g.add((collectie, RDF.type, SOSA.ObservationCollection))
        g.add((collectie, RDF.type, SOSA.ExecutionCollection))
        g.add((collectie, RDFS.label, Literal(f"Jaardebieten van lozingen {jaar}", lang="nl")))
        g.add((collectie, SOSA.observedProperty, pa))
        g.add((collectie, SOSA.phenomenonTime, periode))

    for r in rijen:
        nr, jaar = str(r["Meetput Nummer"]), r["Jaar"]
        meetpunt, lozing = EX[f"meetpunt-{nr}"], EX[f"lozing-{nr}"]
        exploitatie = EX[f"exploitatie-{r['Exploitatie ID']}"]
        obs, res = EX[f"observatie-jaardebiet-{nr}-{jaar}"], EX[f"resultaat-jaardebiet-{nr}-{jaar}"]

        # --- structuur: zelfde IRI's en triples als stap 1 ---
        naam = (r["Exploitatie Naam"] or "").strip()        # 3 exploitaties zonder naam in de bron
        g.add((exploitatie, RDF.type, PROV.Organization))
        if naam:
            g.add((exploitatie, RDFS.label, Literal(naam, lang="nl")))
        g.add((exploitatie, DCTERMS.identifier, Literal(str(r["Exploitatie ID"]))))

        g.add((meetpunt, RDF.type, SOSA.Sampler))
        g.add((meetpunt, RDF.type, PROV.Location))
        g.add((meetpunt, RDFS.label, Literal(f"AW{nr}", lang="nl")))
        ident = EX[f"identificator-meetpunt-{nr}"]
        g.add((meetpunt, ADMS.identifier, ident))
        g.add((ident, RDF.type, ADMS.Identifier))
        g.add((ident, SKOS.notation, Literal(nr)))
        g.add((ident, DCTERMS.creator, vmm))
        if nr in riepr:
            g.add((meetpunt, RDFS.seeAlso, riepr[nr]))    # RIE-IEPR-meetpunt (controle-inrichting)

        g.add((lozing, RDF.type, SOSA.FeatureOfInterest))
        g.add((lozing, RDF.type, PROV.Entity))
        g.add((lozing, RDFS.label, Literal(f"Lozing aan meetput AW{nr}" + (f" ({naam})" if naam else ""), lang="nl")))
        g.add((lozing, PROV.wasAttributedTo, exploitatie))
        g.add((lozing, SOSA.isFeatureOfInterestOf, obs))

        # --- observatie jaardebiet ---
        g.add((EX[f"collectie-jaardebieten-{jaar}"], SOSA.hasMember, obs))
        g.add((obs, RDF.type, SOSA.Observation))
        g.add((obs, RDF.type, SOSA.Execution))
        g.add((obs, RDFS.label, Literal(f"Jaardebiet {jaar} lozing aan meetput AW{nr}", lang="nl")))
        g.add((obs, SOSA.hasFeatureOfInterest, lozing))
        g.add((obs, SOSA.observedProperty, pa))
        g.add((obs, SOSA.hasResult, res))
        g.add((obs, PROV.atLocation, meetpunt))
        databron = r["Databron Jaardebiet"]
        if databron not in DATABRONNEN:
            sys.exit(f"onbekende databron {databron!r} bij meetput {nr}")
        g.add((obs, PROV.used, EX[f"databron-{databron}"]))

        g.add((res, RDF.type, SOSA.Result))
        g.add((res, SOSA.isResultOf, obs))
        g.add((res, QUDT.numericValue, decimaal(r[KOLOM_DEBIET])))
        g.add((res, QUDT.hasUnit, eenheid))
    return g


def schrijf(g, pad, kop):
    with open(pad, "w", encoding="utf-8") as f:
        f.write(kop + g.serialize(format="turtle"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csor", default="~/git/csor", help="map met de codelijst-csor-*-repo's")
    ap.add_argument("--riepr", default=RIEPR_VOORBEELD, help="RIE-IEPR-datavoorbeeld met vmm:lozingspuntCode")
    args = ap.parse_args()

    rijen = json.load(open(BRON, encoding="utf-8"))
    teller = collections.Counter(str(r["Meetput Nummer"]) for r in rijen)
    if max(teller.values()) > 1:
        sys.exit("een meetput komt meermaals voor; IRI-schema (meetput, jaar) is dan niet uniek")
    csor = Csor(args.csor)
    riepr = riepr_meetpunten(args.riepr)
    os.makedirs(UIT, exist_ok=True)

    kop = ("# Jaardebieten van lozingen (VMM, 250129) als SSN/SOSA 2023 -- DIT IS VOORBEELDDATA\n"
           "# Gegenereerd door scripts/afvalwater_debieten.py; niet manueel bewerken.\n")
    volledig = bouw(rijen, csor, riepr)
    schrijf(volledig, os.path.join(UIT, f"{NAAM}.trig"), kop)
    subset = bouw([r for r in rijen if str(r["Meetput Nummer"]) in SUBSET_MEETPUTTEN], csor, riepr)
    schrijf(subset, os.path.join(UIT, f"{NAAM}.ttl"),
            kop + f"# Validatie-subset: AGC Glass Mol, meetputten {', '.join(sorted(SUBSET_MEETPUTTEN))}.\n")
    gekoppeld = sum(1 for nr in teller if nr in riepr)
    print(f"{len(rijen)} rijen -> {len(set(volledig.subjects(RDF.type, SOSA.Observation)))} observaties; "
          f"{len(volledig)} triples; subset {len(subset)} triples; {gekoppeld} meetputten gekoppeld aan RIE-IEPR",
          file=sys.stderr)


if __name__ == "__main__":
    main()
