"""Gedeelde code voor de waterkwaliteit-omzettingen (stap 1, 2, … van stappenplan.md).

- Csor: CSOR-parameter, -parameteraspect en -eenheid opzoeken
  (koppelregels in ../codelijsten.md §3.1–3.3).
- Procedures: jaarversies van de observatieprocedures uit de VITO-lijst.
- decimaal: xsd:decimal zonder float-afrondingsruis.
"""
import collections
import json
import os
import sys
from decimal import Decimal

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, SKOS, XSD

HIER = os.path.dirname(os.path.abspath(__file__))
VITO = os.path.normpath(os.path.join(
    HIER, "..", "brondata_Jurgen", "Lijst_observatiemethodes_VITO-v1", "Observatiemethoden.json"))

SOSA = Namespace("http://www.w3.org/ns/sosa/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
TIME = Namespace("http://www.w3.org/2006/time#")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
CSOR = Namespace("https://data.omgeving.vlaanderen.be/ns/csor#")
MATRIX = Namespace("https://data.omgeving.vlaanderen.be/id/concept/matrix/")
PROCEDURE = Namespace("https://data.omgeving.vlaanderen.be/id/concept/observatieprocedure/")
CSOR_PARAMETERASPECT = Namespace("https://data.omgeving.vlaanderen.be/id/concept/csor/parameteraspect/")
CSOR_EENHEID = Namespace("https://data.omgeving.vlaanderen.be/id/concept/csor/eenheid/")
EPSG31370 = "<http://www.opengis.net/def/crs/EPSG/0/31370>"

_CSOR_B = "src/main/resources/be/vlaanderen/omgeving/data/id/conceptscheme/csor"
_SCHEMA = "https://data.omgeving.vlaanderen.be/id/conceptscheme/csor/"


class Csor:
    """Zoekt CSOR-parameters, -parameteraspecten en -eenheden op in ~/git/csor."""

    def __init__(self, map_):
        self.g = Graph()
        for repo, naam in (("parameter", "parameter"), ("parameteraspect", "parameteraspect"),
                           ("kwantificeerbaar-aspect", "kwantificeerbaaraspect"), ("eenheid", "eenheid"),
                           ("drager", "drager")):
            self.g.parse(os.path.join(os.path.expanduser(map_), f"codelijst-csor-{repo}", _CSOR_B, naam,
                                      f"{naam}.nt"), format="nt")
        self.eenheid = {}
        for e, s in self.g.subject_objects(CSOR.symbool):
            if (e, SKOS.inScheme, URIRef(_SCHEMA + "eenheid")) in self.g and self.actief(e):
                self.eenheid.setdefault(str(s), e)
        parameters = [p for p in self.g.subjects(RDF.type, CSOR.Parameter) if self.actief(p)]
        self.parameter = {str(self.g.value(p, SKOS.notation)): p for p in parameters}
        self.drager = {str(self.g.value(d, SKOS.prefLabel)): d
                       for d in self.g.subjects(SKOS.inScheme, URIRef(_SCHEMA + "drager"))}
        self.parameter_symbool = {}
        for p in parameters:
            s, d = self.g.value(p, CSOR.symbool), self.g.value(p, CSOR.heeftDrager)
            if s is not None and d is not None:
                self.parameter_symbool[(str(s), d)] = p
        self.aspecten = collections.defaultdict(list)
        for pa, p in self.g.subject_objects(CSOR.heeftParameter):
            if self.actief(pa):
                self.aspecten[p].append(pa)

    def actief(self, x):
        return str(self.g.value(x, OWL.deprecated)).lower() != "true"

    def label(self, x):
        return self.g.value(x, SKOS.prefLabel)

    def _aspect(self, p, eenheidssymbool):
        e = self.eenheid.get(eenheidssymbool)
        if p is None or e is None:
            return None, e
        kandidaten = [pa for pa in self.aspecten[p]
                      if (self.g.value(pa, CSOR.heeftAspect), CSOR.toepasbareEenheid, e) in self.g]
        return (kandidaten[0] if len(kandidaten) == 1 else None), e

    def parameteraspect(self, code, eenheidssymbool):
        """Via de CSOR-parametercode (P_…) en het eenheidssymbool."""
        return self._aspect(self.parameter.get(code), eenheidssymbool)

    def parameteraspect_symbool(self, symbool, drager, eenheidssymbool):
        """Via het CSOR-parametersymbool, het label van de drager (bv. 'water') en het eenheidssymbool."""
        return self._aspect(self.parameter_symbool.get((symbool, self.drager.get(drager))), eenheidssymbool)


class Procedures:
    """Jaarversies van de observatieprocedures uit de VITO-lijst: (hoofdprocedure, jaar) -> record."""

    def __init__(self, pad=VITO):
        rijen = json.load(open(pad, encoding="utf-8"))
        self.hoofd = {URIRef(r["URI"]): r for r in rijen if not r["Is versie van"]}
        self.versie = {(URIRef(r["Is versie van"]), int(r["Jaar"])): r for r in rijen if r["Is versie van"]}

    def voor(self, hoofd, jaar):
        r = self.versie.get((hoofd, jaar))
        if r is None:
            sys.exit(f"geen jaarversie {jaar} van {hoofd} in de VITO-lijst")
        return r


def decimaal(v):
    return Literal(Decimal(str(v)), datatype=XSD.decimal)
