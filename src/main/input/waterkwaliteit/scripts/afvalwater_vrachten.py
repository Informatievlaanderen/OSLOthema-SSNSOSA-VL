"""Stap 4 van stappenplan.md: vrachten (251013 contrastmiddelen, 240426 PFAS) naar SSN/SOSA 2023.

Invoer:
- ../brondata_Jurgen/251013_AW_Periodevracht_DETS_Prompts_3-contrastmiddelen_geenInEx/per_type_meetput.json
- ../brondata_Jurgen/240426_AW_Vrachten-PFAS_Indaver_3M_excl-totaal-par/Pagina1.json
- CSOR-codelijsten in ~/git/csor (via waterkwaliteit_gemeen.Csor)

Uitvoer (../nieuw_model/afvalwater_vrachten/):
- vrachten_contrastmiddelen.trig / .ttl  (subset: SUBSET_GROEP_JAAR)
- vrachten_pfas.trig / .ttl              (subset: SUBSET_MEETPUT)

Ontwerpregel (stappenplan.md stap 4, beslisdocument.md A7): een afgeleide observatie (vracht)
verwijst met sosa:hasInputValue naar de resultaten (waarden) waaruit ze berekend is, en met
sosa:relatedObservation naar de observaties die die resultaten opleverden. Haar sosa:usedProcedure
declareert de abstracte inputs met sosa:hasInput (CSOR kwantificeerbare aspecten, R5); SOSA 2023:
"the input value MUST be consistent with a hasInput definition from the corresponding Procedure".
Een observatie is een activiteit (sosa:Execution ⊂ prov:Activity), geen waarde. De vracht
is geen lid van de collectie met de bronobservaties (R13). Bronobservaties onderling krijgen
geen koppeling.

251013: FOI = groep van lozingen (categorie lozer x type meetput); per groep en jaar één
debietobservatie (m³, gedeeld door de parameters), per parameter een concentratie-, een bruto-
en een nettovrachtobservatie. Bruto = concentratie x debiet (nagekeken voor alle rijen).
240426: FOI = de lozing (zelfde IRI's als stap 1 en 3), enkel de bruto vracht, zonder inputs.
De exploitantnaam staat op de observatie (ze verandert in de tijd), niet op de lozing.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/afvalwater_vrachten.py [--csor ~/git/csor]

Vereist: rdflib.
"""
import argparse
import collections
import json
import os
import sys

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import DCTERMS, PROV, RDF, RDFS, SKOS, XSD

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from waterkwaliteit_gemeen import CSOR, MATRIX, QUDT, SOSA, TIME, WK, Csor, decimaal  # noqa: E402

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.normpath(os.path.join(HIER, "..", "brondata_Jurgen"))
CONTRAST = os.path.join(BRON, "251013_AW_Periodevracht_DETS_Prompts_3-contrastmiddelen_geenInEx", "per_type_meetput.json")
PFAS = os.path.join(BRON, "240426_AW_Vrachten-PFAS_Indaver_3M_excl-totaal-par", "Pagina1.json")
UIT = os.path.normpath(os.path.join(HIER, "..", "nieuw_model", "afvalwater_vrachten"))
SUBSET_GROEP_JAAR = ("Bedrijven", "RIO", 2014)
SUBSET_MEETPUT = "2030042"   # exploitant wisselt: Antwerp Waste Management (2009) -> Veolia ES MRC (2017, 2022)

EX = Namespace("https://example.org/waterkwaliteit/afvalwater/")   # zelfde namespace als stap 1 en 3
KWA = Namespace("https://data.omgeving.vlaanderen.be/id/concept/csor/kwantificeerbaaraspect/")


def nieuwe_graaf():
    g = Graph()
    for p, ns in (("ex", EX), ("sosa", SOSA), ("qudt", QUDT), ("time", TIME), ("prov", PROV), ("dct", DCTERMS),
                  ("skos", SKOS), ("xsd", XSD), ("rdfs", RDFS), ("matrix", MATRIX), ("csor-kwa", KWA), ("wk", WK),
                  ("csor-parameteraspect", "https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/"),
                  ("csor-eenheid", "https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/"), ("csor", CSOR)):
        g.bind(p, ns)
    return g


def label(g, iri, tekst):
    g.add((iri, RDFS.label, Literal(str(tekst), lang="nl")))


def periode(g, jaar):
    """Kalenderjaar als half-open time:Interval (R12); zelfde IRI's en triples als stap 3."""
    p = EX[f"periode-{jaar}"]
    begin, einde = EX[f"tijdstip-{jaar}-01-01T000000"], EX[f"tijdstip-{jaar + 1}-01-01T000000"]
    g.add((p, RDF.type, TIME.Interval))
    g.add((p, TIME.hasBeginning, begin))
    g.add((p, TIME.hasEnd, einde))
    for t, j in ((begin, jaar), (einde, jaar + 1)):
        g.add((t, RDF.type, TIME.Instant))
        g.add((t, TIME.inXSDDateTime, Literal(f"{j}-01-01T00:00:00", datatype=XSD.dateTime)))
    return p


class Koppeling:
    """CSOR-opzoekingen met minimale type-asserties in de graaf (sosa:Property, labels)."""

    def __init__(self, csor, g):
        self.csor, self.g, self.gezien = csor, g, set()

    def _extern(self, iri, typen):
        if iri not in self.gezien:
            self.gezien.add(iri)
            for t in typen:
                self.g.add((iri, RDF.type, t))
            label(self.g, iri, self.csor.label(iri))

    def aspect(self, pa_en_eenheid, wat):
        pa, eenheid = pa_en_eenheid
        if pa is None or eenheid is None:
            sys.exit(f"geen eenduidig CSOR-parameteraspect voor {wat}")
        self._extern(pa, (SOSA.Property, CSOR.ParameterAspect))
        self._extern(eenheid, (CSOR.Eenheid,))
        return pa, eenheid

    def kwa(self, pa):
        """Het CSOR kwantificeerbaar aspect van een parameteraspect (abstract input-/outputtype)."""
        k = self.csor.g.value(pa, CSOR.heeftAspect)
        self._extern(k, (SKOS.Concept, CSOR.KwantificeerbaarAspect))
        return k


def procedures(g, k, concentratie_pa, debiet_pa, vracht_pa):
    """Berekeningsprocedures bruto en netto vracht; hasInput/hasOutput = kwantificeerbare aspecten."""
    bruto, netto = EX["procedure-bruto-vracht"], EX["procedure-netto-vracht"]
    for p in (bruto, netto):
        g.add((p, RDF.type, SOSA.ObservingProcedure))
        g.add((p, RDF.type, SOSA.Procedure))
        g.add((p, SOSA.hasOutput, k.kwa(vracht_pa)))
    label(g, bruto, "Berekening bruto vracht: concentratie × debiet over de periode")
    g.add((bruto, RDFS.comment, Literal("Bruto vracht (mg) = concentratie (µg/L) × debiet (m³). Nagekeken op alle "
                                        "rijen van 251013. Concentratie en debiet zijn de 'OG'-waarden van de bron.",
                                        lang="nl")))
    if concentratie_pa is not None:
        g.add((bruto, SOSA.hasInput, k.kwa(concentratie_pa)))
    if debiet_pa is not None:
        g.add((bruto, SOSA.hasInput, k.kwa(debiet_pa)))
    label(g, netto, "Berekening netto vracht")
    g.add((netto, RDFS.comment, Literal("Berekeningswijze niet in de bron; in 251013 gelijk aan de bruto vracht "
                                        "(bestand 'geenInEx'). Te bevestigen door de VMM (stappenplan.md V10).",
                                        lang="nl")))
    return bruto, netto


def resultaat(g, res, obs, waarde, eenheid):
    g.add((res, RDF.type, SOSA.Result))
    g.add((res, RDF.type, WK.Meetresultaat))  # AP (beslisdocument.md A15)
    g.add((res, SOSA.isResultOf, obs))
    g.add((res, QUDT.numericValue, decimaal(waarde)))
    g.add((res, QUDT.hasUnit, eenheid))


def observatie(g, obs, foi, pa, tijd=None, lbl=None):
    g.add((obs, RDF.type, SOSA.Observation))
    g.add((obs, RDF.type, WK.WaterkwaliteitObservatie))  # AP (beslisdocument.md A15)
    g.add((obs, RDF.type, SOSA.Execution))
    g.add((obs, SOSA.hasFeatureOfInterest, foi))
    g.add((obs, SOSA.observedProperty, pa))
    g.add((foi, SOSA.isFeatureOfInterestOf, obs))
    if tijd is not None:
        g.add((obs, SOSA.phenomenonTime, tijd))
    if lbl:
        label(g, obs, lbl)


def contrastmiddelen(rijen, csor):
    g = nieuwe_graaf()
    k = Koppeling(csor, g)
    afvalwater = MATRIX["afvalwater"]
    g.add((afvalwater, RDF.type, SKOS.Concept))
    label(g, afvalwater, "Afvalwater")
    debiet_pa, debiet_e = k.aspect(csor.parameteraspect_symbool("Q", "water", "m³"), "debiet (m³)")
    eerste = rijen[0]
    conc_pa0, _ = k.aspect(csor.parameteraspect(eerste["Parameter Code"], eerste["Conc Eenheid"]), "concentratie")
    vracht_pa0, _ = k.aspect(csor.parameteraspect(eerste["Parameter Code"], eerste["Vracht Eenheid"]), "vracht")
    bruto_proc, netto_proc = procedures(g, k, conc_pa0, debiet_pa, vracht_pa0)

    for r in rijen:
        cat, code, jaar, p = r["Bedrijven/RWZI"], r["SP Type Code"], r["Jaar"], r["Parameter Code"]
        slug = f"{cat.lower()}-{code.lower()}"
        groep = EX[f"lozingsgroep-{slug}"]
        g.add((groep, RDF.type, WK.Emissie))            # beslisdocument.md A14
        g.add((groep, RDF.type, SOSA.FeatureOfInterest))
        g.add((groep, RDF.type, PROV.Entity))
        g.add((groep, DCTERMS.type, afvalwater))
        g.add((groep, DCTERMS.identifier, Literal(f"{cat}/{code}")))
        label(g, groep, f"Lozingen van {cat.lower()} — type meetput {r['SP Type Omschrijving'].lower()}")
        tijd = periode(g, jaar)

        # bronobservaties: debiet (per groep en jaar) en concentratie (per parameter), samen in een collectie
        collectie = EX[f"collectie-vrachtbronnen-{slug}-{jaar}"]
        g.add((collectie, RDF.type, SOSA.ObservationCollection))
        g.add((collectie, RDF.type, WK.WaterkwaliteitObservatieVerzameling))  # AP (beslisdocument.md A15)
        g.add((collectie, RDF.type, SOSA.ExecutionCollection))
        label(g, collectie, f"Concentraties en debiet {jaar}, lozingen van {cat.lower()} ({r['SP Type Omschrijving']})")
        g.add((collectie, SOSA.hasFeatureOfInterest, groep))
        g.add((collectie, SOSA.phenomenonTime, tijd))
        g.add((groep, SOSA.isFeatureOfInterestOf, collectie))

        deb, deb_res = EX[f"observatie-debiet-{slug}-{jaar}"], EX[f"resultaat-debiet-{slug}-{jaar}"]
        observatie(g, deb, groep, debiet_pa)
        g.add((deb, SOSA.hasResult, deb_res))
        resultaat(g, deb_res, deb, r["Debiet (m³)"], debiet_e)
        g.add((collectie, SOSA.hasMember, deb))

        conc_pa, conc_e = k.aspect(csor.parameteraspect(p, r["Conc Eenheid"]), f"concentratie {p}")
        conc, conc_res = EX[f"observatie-concentratie-{slug}-{jaar}-{p}"], EX[f"resultaat-concentratie-{slug}-{jaar}-{p}"]
        observatie(g, conc, groep, conc_pa)
        g.add((conc, SOSA.hasResult, conc_res))
        resultaat(g, conc_res, conc, r["Conc OG"], conc_e)
        g.add((collectie, SOSA.hasMember, conc))

        # afgeleide observaties: bruto en netto vracht (geen lid van de collectie, R13)
        vracht_pa, vracht_e = k.aspect(csor.parameteraspect(p, r["Vracht Eenheid"]), f"vracht {p}")
        bruto = EX[f"observatie-brutovracht-{slug}-{jaar}-{p}"]
        observatie(g, bruto, groep, vracht_pa, tijd, f"Bruto vracht {r['Parameter Omschrijving']} {jaar}, "
                                                      f"lozingen van {cat.lower()} ({r['SP Type Omschrijving']})")
        g.add((bruto, SOSA.usedProcedure, bruto_proc))
        g.add((bruto, SOSA.hasInputValue, conc_res))          # de waarden (KWA_1, KWA_10)
        g.add((bruto, SOSA.hasInputValue, deb_res))
        g.add((bruto, SOSA.relatedObservation, conc))         # de observaties die ze opleverden
        g.add((bruto, SOSA.relatedObservation, deb))
        g.add((bruto, SOSA.hasResult, EX[f"resultaat-brutovracht-{slug}-{jaar}-{p}"]))
        resultaat(g, EX[f"resultaat-brutovracht-{slug}-{jaar}-{p}"], bruto, r["Bruto Vracht OG"], vracht_e)

        netto = EX[f"observatie-nettovracht-{slug}-{jaar}-{p}"]
        observatie(g, netto, groep, vracht_pa, tijd, f"Netto vracht {r['Parameter Omschrijving']} {jaar}, "
                                                      f"lozingen van {cat.lower()} ({r['SP Type Omschrijving']})")
        g.add((netto, SOSA.usedProcedure, netto_proc))
        g.add((netto, SOSA.relatedObservation, bruto))      # associatief: berekeningswijze onbekend
        g.add((netto, SOSA.hasResult, EX[f"resultaat-nettovracht-{slug}-{jaar}-{p}"]))
        resultaat(g, EX[f"resultaat-nettovracht-{slug}-{jaar}-{p}"], netto, r["Netto Vracht OG"], vracht_e)
    return g


def pfas(rijen, csor):
    g = nieuwe_graaf()
    k = Koppeling(csor, g)
    afvalwater = MATRIX["afvalwater"]
    g.add((afvalwater, RDF.type, SKOS.Concept))
    label(g, afvalwater, "Afvalwater")
    # dezelfde bruto-vrachtprocedure; de inputs (concentratie, debiet) zijn niet aangeleverd
    eerste = rijen[0]
    vracht_pa0, _ = k.aspect(csor.parameteraspect_symbool(eerste["Symbool"], "water",
                                                          eerste["Standaard Vracht Eenheid Symbool MAW"]), "vracht")
    conc_pa0, _ = k.aspect(csor.parameteraspect_symbool(eerste["Symbool"], "water", "µg/L"), "concentratie")
    debiet_pa, _ = k.aspect(csor.parameteraspect_symbool("Q", "water", "m³"), "debiet (m³)")
    bruto_proc, _ = procedures(g, k, conc_pa0, debiet_pa, vracht_pa0)

    for r in rijen:
        nr, jaar = str(r["Meetput Nummer"]), r["Meetput JV Jaar Datum DTS"]
        lozing = EX[f"lozing-{nr}"]
        g.add((lozing, RDF.type, WK.Emissie))           # beslisdocument.md A14
        g.add((lozing, RDF.type, SOSA.FeatureOfInterest))   # zelfde IRI als stap 1 en 3; geen label hier:
        g.add((lozing, RDF.type, PROV.Entity))              # de exploitant wisselt in de tijd (zie observatie)
        g.add((lozing, DCTERMS.type, afvalwater))
        pa, e = k.aspect(csor.parameteraspect_symbool(r["Symbool"], "water",
                                                      r["Standaard Vracht Eenheid Symbool MAW"]), r["Symbool"])
        code = str(pa).rsplit("/", 1)[1]
        obs, res = EX[f"observatie-brutovracht-{nr}-{jaar}-{code}"], EX[f"resultaat-brutovracht-{nr}-{jaar}-{code}"]
        observatie(g, obs, lozing, pa, periode(g, jaar),
                   f"Bruto jaarvracht {r['Symbool']} {jaar}, meetput AW{nr} ({r['Exploitatie Naam'].strip()})")
        g.add((obs, SOSA.usedProcedure, bruto_proc))
        g.add((obs, SOSA.hasResult, res))
        resultaat(g, res, obs, r["Meetput JV M Bruto Vracht OG DTS"], e)
    return g


def schrijf(g, pad, kop):
    with open(pad, "w", encoding="utf-8") as f:
        f.write(kop + g.serialize(format="turtle"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csor", default="~/git/csor", help="map met de codelijst-csor-*-repo's")
    args = ap.parse_args()
    csor = Csor(args.csor)
    os.makedirs(UIT, exist_ok=True)

    rc = json.load(open(CONTRAST, encoding="utf-8"))
    for r in rc:   # bruto = concentratie x debiet (µg/L x m³ = mg)
        if abs(r["Conc OG"] * r["Debiet (m³)"] - r["Bruto Vracht OG"]) > 1e-6 * max(1, r["Bruto Vracht OG"]):
            sys.exit(f"bruto vracht is niet concentratie x debiet: {r}")
    deb = collections.defaultdict(set)
    for r in rc:
        deb[(r["Bedrijven/RWZI"], r["SP Type Code"], r["Jaar"])].add(r["Debiet (m³)"])
    if any(len(v) > 1 for v in deb.values()):
        sys.exit("debiet verschilt per parameter binnen een groep en jaar: één debietobservatie volstaat niet")
    kop = "# {} (VMM, {}) als SSN/SOSA 2023 -- DIT IS VOORBEELDDATA\n# Gegenereerd door scripts/afvalwater_vrachten.py; niet manueel bewerken.\n"
    k1 = kop.format("Periodevrachten contrastmiddelen", "251013")
    schrijf(contrastmiddelen(rc, csor), os.path.join(UIT, "vrachten_contrastmiddelen.trig"), k1)
    sub = [r for r in rc if (r["Bedrijven/RWZI"], r["SP Type Code"], r["Jaar"]) == SUBSET_GROEP_JAAR]
    schrijf(contrastmiddelen(sub, csor), os.path.join(UIT, "vrachten_contrastmiddelen.ttl"),
            k1 + f"# Validatie-subset: {SUBSET_GROEP_JAAR[0]} / {SUBSET_GROEP_JAAR[1]} / {SUBSET_GROEP_JAAR[2]}.\n")

    rp = json.load(open(PFAS, encoding="utf-8"))
    k2 = kop.format("Jaarvrachten PFAS", "240426")
    schrijf(pfas(rp, csor), os.path.join(UIT, "vrachten_pfas.trig"), k2)
    schrijf(pfas([r for r in rp if str(r["Meetput Nummer"]) == SUBSET_MEETPUT], csor),
            os.path.join(UIT, "vrachten_pfas.ttl"), k2 + f"# Validatie-subset: meetput {SUBSET_MEETPUT}.\n")
    print(f"contrastmiddelen: {len(rc)} rijen, {len(deb)} groep-jaren; PFAS: {len(rp)} rijen -> {UIT}", file=sys.stderr)


if __name__ == "__main__":
    main()
