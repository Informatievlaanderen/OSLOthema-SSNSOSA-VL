"""Toetst de CSOR-registerdata aan de I-ADOPT-rollen: wat is verkeerd getypeerd, wat staat niet op
zijn plaats (zie ../csor_iadopt.md §9).

Invoer:  parameteraspect_matrix.csv uit csor-testing (één rij per actief parameteraspect, met
         variabele, parameter, drager, soort waardebepaling, aspect en dimensie):
         ~/git/csor/csor-testing/output/tables/parameteraspect_matrix.csv
         en de parameteraspecten die de waterkwaliteitsvoorbeelden gebruiken (../nieuw_model).
Uitvoer: ../csor_iadopt/
    variabele_rol.csv            per variabele: I-ADOPT-rol, op zijn plaats (ja/grensgeval/nee), reden
    soortwaardebepaling_rol.csv  per soort waardebepaling: categorie, plaats volgens I-ADOPT/SOSA
    drager_rol.csv               per drager
    aspect_rol.csv               per kwantificeerbaar/kwalificeerbaar aspect: ingebedde componenten,
                                 dimensiefouten
    dimensie_rol.csv             natuurkundige dimensies die geen dimensie zijn
    parameteraspect_afwijkingen.csv
                                 per parameteraspect met minstens één afwijking: de afwijkingen,
                                 en of het in de waterkwaliteitsvoorbeelden gebruikt wordt
    samenvatting.csv             tellingen per toets (alle actieve / gebruikt in waterkwaliteit)

De indeling is regelgebaseerd (label, collectie, CAS/InChIKey, aspect). De regels staan bovenaan
als tabellen, zodat een CSOR-beheerder ze kan nalezen en bijsturen.

Gebruik (vanuit om het even welke werkmap):
    python3 scripts/csor_iadopt_toets.py [pad/naar/parameteraspect_matrix.csv]

Vereist: enkel de standaardbibliotheek.
"""
import collections
import csv
import glob
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
WK = os.path.normpath(os.path.join(HIER, ".."))
MATRIX = os.path.expanduser("~/git/csor/csor-testing/output/tables/parameteraspect_matrix.csv")
UIT = os.path.join(WK, "csor_iadopt")

# ---------------------------------------------------------------------------
# Regels: soort waardebepaling (alle 80 waarden in het register; enkel de gebruikte komen in de CSV)
# categorie -> (plaats volgens I-ADOPT/SOSA, op zijn plaats in de parameter?)
# ---------------------------------------------------------------------------
SWB_CATEGORIE = {
    "geen beperking": ("geen component", "ja"),
    "fractie of vorm": ("iadopt:Constraint op ObjectOfInterest of matrix", "ja"),
    "voorbehandeling": ("iadopt:Constraint (de bekomen fractie); de test zelf is een sosa:Procedure", "grensgeval"),
    "ecotoxicologisch eindpunt of duur": ("iadopt:Property (EC50/LC50) + iadopt:Constraint (blootstellingsduur)", "nee"),
    "statistiek": ("iadopt:StatisticalModifier", "nee"),
    "analysemethode": ("sosa:usedProcedure op de observatie", "nee"),
    "staalnametoestel": ("sosa:Sampler / staalnameprocedure", "nee"),
    "project": ("provenance van de observatie (prov:wasGeneratedBy, dct:source)", "nee"),
    "berekening": ("sosa:Procedure van een afgeleide observatie", "nee"),
}
SWB_REGELS = [  # (regex op label, categorie); eerste treffer wint
    (r"^standaard$", "geen beperking"),
    (r"MUC", "project"),
    (r"^(GC-MS|LC-MS)$", "analysemethode"),
    (r"sampler", "staalnametoestel"),
    (r"deviatie", "statistiek"),
    (r"indexberekening", "berekening"),
    (r"EC50|LC50|inhibitie|luminiscentie|lum-inh|^\d+h( na Zahn Wellens)?$", "ecotoxicologisch eindpunt of duur"),
    (r"Eluaat|Zahn Wellens|extraheerbaar|vrijstelbaar|na 120h|warm", "voorbehandeling"),
    (r".", "fractie of vorm"),
]

# ---------------------------------------------------------------------------
# Regels: drager
# ---------------------------------------------------------------------------
DRAGER = {
    "water": ("matrix", "iadopt:hasMatrix", "ja", ""),
    "lucht": ("matrix", "iadopt:hasMatrix", "ja", ""),
    "vaste deel van de aarde": ("matrix", "iadopt:hasMatrix", "ja", ""),
    "biota": ("matrix", "iadopt:hasMatrix", "ja", "algemeen; het organisme(deel) staat op het staal"),
    "regen": ("matrix", "iadopt:hasMatrix", "ja", ""),
    "PM10": ("matrix (deeltjesfractie)", "iadopt:hasMatrix, lucht als iadopt:hasContextObject", "ja",
             "PM10 is een matrix in lucht; ook als variabele V_1901 gebruikt (dan ObjectOfInterest)"),
    "PM2.5": ("matrix (deeltjesfractie)", "iadopt:hasMatrix, lucht als iadopt:hasContextObject", "ja",
              "idem; ook variabele V_1902"),
    "TSP": ("matrix (deeltjesfractie)", "iadopt:hasMatrix, lucht als iadopt:hasContextObject", "ja", ""),
    "bulk depositie (precip)": ("matrix + staalnamewijze", "matrix neerslag + iadopt:Constraint of staalnameprocedure",
                                "grensgeval", "'bulk' is een staalnamewijze (open collector)"),
    "wet-only depositie (prec)": ("matrix + staalnamewijze", "matrix neerslag + iadopt:Constraint of staalnameprocedure",
                                  "grensgeval", "'wet-only' is een staalnamewijze (gesloten collector)"),
    "materiaal": ("onbepaald", "geen extern koppelbare matrix", "grensgeval",
                  "welk materiaal (afval, product, bouwstof) staat nergens; nodig om de matrix te benoemen"),
    "passiveSamplingFilter": ("staalnametoestel", "sosa:Sampler", "nee", "geen actieve parameter gebruikt het"),
}

# ---------------------------------------------------------------------------
# Regels: variabele (eerste treffer wint; volgorde is betekenisvol)
# rol -> (I-ADOPT-rol, op zijn plaats, wat er moet gebeuren)
# ---------------------------------------------------------------------------
ROL = {
    "stof": ("iadopt:Entity (ObjectOfInterest)", "ja", ""),
    "stof in verkeerde collectie": ("iadopt:Entity (ObjectOfInterest)", "grensgeval",
                                    "stof (CAS/InChIKey, mineraal, pigment) in fysische_eigenschappen of bio_indicatoren: collectie aanpassen"),
    "stofgroep": ("iadopt:Entity (ObjectOfInterest); iadopt:SymmetricSystem als de delen gekend zijn", "ja", ""),
    "verschil (rekenregel)": ("buiten I-ADOPT: rekenregel", "nee",
                              "geen entiteit; hoort als ParameterAfleiding, niet als variabele"),
    "verzamelnaam 'individueel'": ("geen", "nee",
                                   "verwijst naar een verzameling losse stoffen, niet naar één ObjectOfInterest"),
    "methodegedefinieerde grootheid": ("iadopt:Property (de methode bepaalt de grootheid); ObjectOfInterest = drager", "grensgeval",
                                       "eigenschap staat in de variabele; drager wordt ObjectOfInterest"),
    "deeltjes of materiaalfractie": ("iadopt:Entity (ObjectOfInterest), operationeel afgebakend", "grensgeval",
                                     "afbakening (grootte, methode) als iadopt:Constraint beschrijven"),
    "eigenschap": ("iadopt:Property; ObjectOfInterest = drager", "nee",
                   "eigenschap staat in de variabele én in het aspect; drager wordt ObjectOfInterest"),
    "eigenschap met statistiek": ("iadopt:Property + iadopt:StatisticalModifier", "nee",
                                  "statistiek (min/max/verschil) hoort niet in de variabele"),
    "eigenschap met methode of conditie": ("iadopt:Property + iadopt:Constraint; methode = sosa:Procedure", "nee",
                                           "meetconditie of methode staat in het label van de variabele"),
    "afgeleide verhouding of rendement": ("iadopt:Property (verhouding) met iadopt:AsymmetricSystem", "nee",
                                          "berekening; hoort als ParameterAfleidingVerhouding/-Rendement"),
    "organisme (studieobject)": ("iadopt:Entity (ObjectOfInterest)", "ja", ""),
    "testorganisme (ecotoxicologie)": ("iadopt:hasContextObject; ObjectOfInterest = het geteste staal", "nee",
                                       "het organisme is het meetinstrument van de toets, niet wat bestudeerd wordt"),
    "bioassay": ("sosa:Procedure; ObjectOfInterest = het staal, Property = equivalente activiteit", "nee",
                 "een toets (CALUX, Microtox) is een procedure, geen variabele"),
    "biologisch kwaliteitselement of index": ("iadopt:Property (EKC/index) van het waterlichaam; kwaliteitselement = iadopt:hasContextObject",
                                              "grensgeval", "beoordeling, geen meting van een stof of organisme"),
}
STAT = r"^(Maximale|Minimale) |Temperatuursverschil"
METHODE = r"\((20|25)°C\)|ter plaatse|\(KCl\)|na ontgassen|105°C|FTIR|Pyr-GC-MS| [–-] \d+ nm$"
VERHOUDING = r"Rendement|verhouding|Inwonersequivalent"
METHODEGROOTHEID = (r"Kjeldahl|zuurstofverbruik|BZV|CZV|Permanganaatverbruik|[Ii]ndex$|extrah|Methyleenblauw|"
                    r"^Toxiciteit$|^Fytotox$|^Screening$|gisting|Alkaliniteit met|Potentieel Bioaccumulerende|"
                    r"Solventgehalte|Droogrest|Gloei|Asgehalte|Droge stof|Vochtgehalte|Vetgehalte|Biodegradeerbaarheid|"
                    r"Oxidatief Potentieel|Vlampunt|Hardheid|Alka[a-z]*iteit|Ionenbalans|Organisch materiaal|Organische stof$")
FRACTIE = (r"^PM|^Stof, totaal$|^Zwevende stof|^Vluchtige stof$|^Zwarte (koolstof|rook)|^Latex$|Microplastics|"
           r"Rubber-partikels|Textielvezels|^Bezinkbare stoffen$|Korrelgrootte|Deeltjesaantal|deeltjesaantal|Sedimentgehalte|"
           r"niet vlottende|^Kalk en organische stof$|Filterverzadiging")
BIOASSAY = r"[Cc]alux|CALUX|Microtox|^Cholinesteraseremmers$"
MINERAAL = r"^(Asbest|Calciet)$"
EFFECT_ASPECT = {"effecteenheid", "percentage effect", "percentage mortaliteit"}

# ---------------------------------------------------------------------------
# Regels: eigenschap-variabelen en hun toegelaten dimensies (dimensietoets op parameteraspect)
# ---------------------------------------------------------------------------
DIMENSIE_VAN_EIGENSCHAP = [
    (r"Temperatuur|Dauwpunt|Vlampunt", {"temperatuur"}),
    (r"^pH|Zuurtegraad", {"Geen"}),
    (r"Geleidbaarheid", {"elektrische geleidbaarheid per lengte"}),
    (r"^Debiet$", {"volume per tijdseenheid"}),
    (r"^Volume$", {"volume", "volume per oppervlakte"}),
    (r"^(Lengte|Breedte|Dikte|Bemonsteringsdiepte|Doorzichtigheid|Zwevende stoffen, afmeting)$", {"lengte"}),
    (r"^Redox", {"spanning"}),
    (r"^Turbiditeit$", {"turbiditeit"}),
    (r"^Neerslag$", {"lengte per tijdseenheid", "lengte", "volume per oppervlakte"}),
    (r"Luchtdruk", {"druk"}),
    (r"Windrichting", {"hoek"}),
    (r"Windsnelheid", {"lengte per tijdseenheid"}),
    (r"vochtigheid|Saliniteit", {"dimensieloze verhouding", "Geen"}),
    (r"Straling", {"vermogen per oppervlakte"}),
    (r"Radioactiviteit", {"radioactiviteit per volume"}),
    (r"^Gewicht$", {"massa"}),
]

# ---------------------------------------------------------------------------
# Regels: aspect
# ---------------------------------------------------------------------------
GEEN_GROOTHEID = {  # aspect-id -> reden
    "KWA_15": "'geen' benoemt geen grootheid; de grootheid staat dan enkel in de variabele",
    "KWA_18": "'bezinkbare stoffen' is een ObjectOfInterest, geen grootheid",
    "KWA_22": "'neerslag' is een fenomeen, geen grootheid (de grootheid is neerslaghoogte per tijd)",
    "KWA_103": "'per filter' noemt het staalnametoestel in de grootheid",
}
ELEMENT = r"(fosfor|stikstof|koolstof|zuurstof|chloor|zwavel|tin|ammonium|P2O5|CaCO3|SiO2|Fluor|fluor)\b"
BASIS = r"droge stof|nat gewicht"
CONDITIE = r"\(Nm³\)"
EQUIVALENT = r"TEQ|equivalent"
DIMENSIEFOUT = {
    "KWA_10": "label 'debiet' voor een volume over een periode (dimensie volume, eenheden m³, L): een debiet is volume per tijd",
    "KWA_24": "molvracht met dimensie 'mol' (een eenheid, geen dimensie; verwacht: hoeveelheid stof)",
    "KWA_17": "turbiditeit: gebruikt door variabelen die geen troebelheid zijn (zie parameteraspecten)",
}
GEEN_DIMENSIE = {
    "Geen": "geen dimensie: gebruik 'dimensieloos'",
    "inwonersequivalent": "afgeleide rekeneenheid, geen dimensie",
    "mol": "eenheid, geen dimensie (dimensie = hoeveelheid stof)",
    "Effect eenheden": "toetsspecifieke rekeneenheid, geen dimensie",
    "arbitraire eenheid per volume": "arbitraire eenheid, geen dimensie",
}


def eerste(regels, tekst):
    for patroon, waarde in regels:
        if re.search(patroon, tekst):
            return waarde
    return None


def rol_van_variabele(v, aspecten):
    label, col = v["variabele_label"], v["variabele_collectie"]
    stof = v["variabele_cas"] == "True" or v["variabele_inchikey"] == "True"
    if label.startswith("="):
        return "verschil (rekenregel)"
    if re.search(r"individueel|, ind\.$", label):
        return "verzamelnaam 'individueel'"
    if col == "bio_indicatoren":
        if stof or re.search(r"Chlorofyl", label):
            return "stof in verkeerde collectie"
        if re.search(BIOASSAY, label):
            return "bioassay"
        if "ecologische kwaliteitscoëfficiënt" in aspecten or re.search(r"[Ii]ndex|Trofisch", label):
            return "biologisch kwaliteitselement of index"
        if aspecten & EFFECT_ASPECT:
            return "testorganisme (ecotoxicologie)"
        return "organisme (studieobject)"
    if col in ("chemische_stoffen", "groepsparameters") and stof:
        return "stof" if col == "chemische_stoffen" else "stofgroep"
    if stof or re.search(MINERAAL, label):
        return "stof in verkeerde collectie"
    if col == "chemische_stoffen":
        return "stof"
    if re.search(STAT, label):
        return "eigenschap met statistiek"
    if re.search(VERHOUDING, label):
        return "afgeleide verhouding of rendement"
    if re.search(METHODE, label):
        return "eigenschap met methode of conditie"
    if re.search(FRACTIE, label):
        return "deeltjes of materiaalfractie"
    if re.search(METHODEGROOTHEID, label):
        return "methodegedefinieerde grootheid"
    if "ecologische kwaliteitscoëfficiënt" in aspecten:
        return "biologisch kwaliteitselement of index"
    if col == "groepsparameters":
        return "stofgroep"
    return "eigenschap"


def ingebed(aspect_id, label, uitgedrukt):
    """Componenten die naast de grootheid in het aspect zitten (I-ADOPT: Constraint of eigen Property)."""
    delen = []
    if re.search(ELEMENT, label):
        delen.append("uitgedrukt als element/verbinding" + ("" if uitgedrukt else " (uitgedruktIn ontbreekt)"))
    if re.search(BASIS, label):
        delen.append("basis van de matrix (droog/nat)")
    if re.search(CONDITIE, label):
        delen.append("referentiecondities (Nm³)")
    if re.search(EQUIVALENT, label):
        delen.append("equivalent t.o.v. referentiestof")
    if aspect_id == "KWA_86":
        delen.append("per productie (emissiefactor)")
    return delen


def schrijf(pad, kolommen, rijen):
    with open(pad, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kolommen)
        w.writerows(rijen)


def main():
    matrix = sys.argv[1] if len(sys.argv) > 1 else MATRIX
    with open(matrix, encoding="utf-8") as f:
        rijen = list(csv.DictReader(f))
    gebruikt = set()
    for pad in glob.glob(os.path.join(WK, "nieuw_model", "*", "*.trig")):
        with open(pad, encoding="utf-8") as f:
            gebruikt |= set(re.findall(r"PAS_\d+", f.read()))
    os.makedirs(UIT, exist_ok=True)

    # --- variabelen
    per_var = collections.defaultdict(list)
    for r in rijen:
        per_var[r["variabele_id"]].append(r)
    var_rol = {}
    var_uit = []
    for vid, rs in sorted(per_var.items(), key=lambda kv: int(kv[0][2:])):
        v = rs[0]
        aspecten = {r["aspect_label"] for r in rs}
        rol = rol_van_variabele(v, aspecten)
        var_rol[vid] = rol
        iadopt, plaats, reden = ROL[rol]
        n_gebruikt = sum(r["parameteraspect_id"] in gebruikt for r in rs)
        var_uit.append([vid, v["variabele_label"], v["variabele_collectie"], v["variabele_cas"], rol, iadopt,
                        plaats, reden, len(rs), n_gebruikt])
    schrijf(os.path.join(UIT, "variabele_rol.csv"),
            ["variabele", "label", "collectie", "cas", "rol", "iadopt", "op_zijn_plaats", "reden",
             "n_parameteraspecten", "n_gebruikt_waterkwaliteit"], var_uit)

    # --- soort waardebepaling
    swb = {}
    for r in rijen:
        swb.setdefault(r["swb_id"], [r["swb_label"], set(), 0])
        swb[r["swb_id"]][1].add(r["parameter_id"])
        swb[r["swb_id"]][2] += r["parameteraspect_id"] in gebruikt
    swb_cat = {}
    swb_uit = []
    for sid, (label, params, n_geb) in sorted(swb.items(), key=lambda kv: int(kv[0][4:])):
        cat = eerste(SWB_REGELS, label)
        swb_cat[sid] = cat
        plaats, ok = SWB_CATEGORIE[cat]
        swb_uit.append([sid, label, cat, plaats, ok, len(params), n_geb])
    schrijf(os.path.join(UIT, "soortwaardebepaling_rol.csv"),
            ["soortwaardebepaling", "label", "categorie", "plaats_iadopt_sosa", "op_zijn_plaats",
             "n_parameters", "n_gebruikt_waterkwaliteit"], swb_uit)

    # --- drager
    dr = {}
    for r in rijen:
        dr.setdefault(r["drager_id"], [r["drager_label"], set()])[1].add(r["parameter_id"])
    schrijf(os.path.join(UIT, "drager_rol.csv"),
            ["drager", "label", "soort", "iadopt", "op_zijn_plaats", "opmerking", "n_parameters"],
            [[did, label, *DRAGER[label], len(p)] for did, (label, p) in sorted(dr.items(), key=lambda kv: int(kv[0][3:]))])

    # --- aspect
    asp = {}
    for r in rijen:
        a = asp.setdefault(r["aspect_id"], {"label": r["aspect_label"], "soort": r["aspect_soort"],
                                            "dim": r["dimensie_label"], "uit": r["uitgedruktin_label"],
                                            "pas": set(), "var": set()})
        a["pas"].add(r["parameteraspect_id"])
        a["var"].add(r["variabele_id"])
    asp_afw = {}
    asp_uit = []
    for aid, a in sorted(asp.items(), key=lambda kv: (kv[0][:3], int(kv[0][4:]))):
        delen = ingebed(aid, a["label"], a["uit"])
        fouten = [GEEN_GROOTHEID[aid]] if aid in GEEN_GROOTHEID else []
        if aid in DIMENSIEFOUT:
            fouten.append(DIMENSIEFOUT[aid])
        if any("ontbreekt" in d for d in delen):
            fouten.append("uitgedruktIn ontbreekt")
        asp_afw[aid] = fouten
        plaats = "nee" if fouten else ("grensgeval" if delen else "ja")
        asp_uit.append([aid, a["label"], a["soort"], a["dim"], a["uit"], "; ".join(delen), "; ".join(fouten),
                        plaats, len(a["pas"]), len(a["var"])])
    schrijf(os.path.join(UIT, "aspect_rol.csv"),
            ["aspect", "label", "soort", "dimensie", "uitgedruktIn", "ingebedde_componenten", "fouten",
             "op_zijn_plaats", "n_parameteraspecten", "n_variabelen"], asp_uit)

    # --- dimensie
    dims = {}
    for r in rijen:
        if r["dimensie_id"]:
            dims.setdefault(r["dimensie_id"], [r["dimensie_label"], set()])[1].add(r["aspect_id"])
    schrijf(os.path.join(UIT, "dimensie_rol.csv"),
            ["dimensie", "label", "probleem", "n_aspecten"],
            [[did, label, GEEN_DIMENSIE[label], len(a)] for did, (label, a) in sorted(dims.items(), key=lambda kv: int(kv[0][3:]))
             if label in GEEN_DIMENSIE])

    # --- parameteraspecten
    pas_uit = []
    tel = collections.Counter()
    for r in rijen:
        afw = []
        rol = var_rol[r["variabele_id"]]
        if ROL[rol][1] == "nee":
            afw.append(f"variabele: {rol}")
        if SWB_CATEGORIE[swb_cat[r["swb_id"]]][1] == "nee":
            afw.append(f"soort waardebepaling: {swb_cat[r['swb_id']]}")
        if DRAGER[r["drager_label"]][2] == "nee":
            afw.append(f"drager: {DRAGER[r['drager_label']][0]}")
        afw += [f"aspect: {f}" for f in asp_afw[r["aspect_id"]]]
        toegelaten = eerste([(p, d) for p, d in DIMENSIE_VAN_EIGENSCHAP], r["variabele_label"]) \
            if rol.startswith("eigenschap") or rol == "methodegedefinieerde grootheid" else None
        if toegelaten and r["dimensie_label"] not in toegelaten:
            afw.append(f"dimensieconflict: '{r['variabele_label']}' met aspect '{r['aspect_label']}' "
                       f"(dimensie {r['dimensie_label']})")
        if r["aspect_id"] == "KWA_17" and r["variabele_label"] != "Turbiditeit":
            afw.append(f"dimensieconflict: '{r['variabele_label']}' met aspect 'turbiditeit'")
        geb = r["parameteraspect_id"] in gebruikt
        for a in afw:
            soort = a.split(":")[0]
            tel[(soort, "alle")] += 1
            tel[(soort, "waterkwaliteit")] += geb
        tel[("parameteraspect met afwijking", "alle")] += bool(afw)
        tel[("parameteraspect met afwijking", "waterkwaliteit")] += bool(afw) and geb
        tel[("parameteraspect", "alle")] += 1
        tel[("parameteraspect", "waterkwaliteit")] += geb
        if afw:
            pas_uit.append([r["parameteraspect_id"], r["parameteraspect_label"], r["variabele_id"],
                            r["parameter_id"], r["swb_id"], r["drager_id"], r["aspect_id"], " | ".join(afw),
                            "ja" if geb else ""])
    pas_uit.sort(key=lambda x: int(x[0][4:]))
    schrijf(os.path.join(UIT, "parameteraspect_afwijkingen.csv"),
            ["parameteraspect", "label", "variabele", "parameter", "soortwaardebepaling", "drager", "aspect",
             "afwijkingen", "gebruikt_waterkwaliteit"], pas_uit)

    soorten = ["parameteraspect", "parameteraspect met afwijking", "variabele", "soort waardebepaling",
               "drager", "aspect", "dimensieconflict"]
    schrijf(os.path.join(UIT, "samenvatting.csv"), ["toets", "alle_actieve", "gebruikt_waterkwaliteit"],
            [[s, tel[(s, "alle")], tel[(s, "waterkwaliteit")]] for s in soorten])
    for s in soorten:
        print(f"{s:32} {tel[(s, 'alle')]:6} {tel[(s, 'waterkwaliteit')]:5}")
    print("rollen variabelen:", collections.Counter(var_rol.values()).most_common())
    print(f"uitvoer in {UIT}")


if __name__ == "__main__":
    main()
