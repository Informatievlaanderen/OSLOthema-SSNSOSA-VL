#!/usr/bin/env python3
"""Pseudonimiseer de ELF-bronbestanden met namen uit De Rode Ridder, deterministisch en consistent.

Naar het voorbeeld van imjvtomjv/src/test/python/anonymize.py: elke echte waarde krijgt een fictieve
waarde die uit een hash van de waarde zelf volgt (geen opzoektabel), zodat dezelfde gemeente, straat of
persoon overal dezelfde fictieve naam krijgt, in de CSV én in de parquet.

Wat wordt vervangen:
  elf_sensors_registratie.csv
    - e-mail van de contactpersoon      → <voornaam>.<naam>@graalburcht.example (schurken)
    - Naam, Voornaam                     → een paar schurken uit De Rode Ridder ('//' blijft '//')
    - Straat                             → <schurk><straat|laan|weg|…>
    - Postcode                           → fictieve postcode (1000–9999)
    - Gemeente                           → <prefix><suffix> (Zwartsteen, Nevelburcht, …)
    Huisnummer, sensor-ID, Jira-sleutel en datums blijven: zonder echte straat en gemeente
    identificeren ze niemand.
  _meetperiode_<ticket>_<sensor>_<gemeente>.parquet
    - de gemeente in de kolom 'meetperiode' en in de bestandsnaam

Gebruik (vanuit src/main/input/elf/; vereist pyarrow):
  python3 scripts/anonimiseer.py --report-only   # toon de afbeelding, schrijf niets
  python3 scripts/anonimiseer.py --apply         # vervang de bronbestanden in source/

Enkel uitvoeren op bestanden die nog echte gegevens bevatten: op reeds gepseudonimiseerde bestanden
leidt het script nieuwe fictieve namen af en gaat de vorige afbeelding verloren.
"""
import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

BRON = Path(__file__).resolve().parent.parent / "source"
CSV = BRON / "elf_sensors_registratie.csv"
PARQUET_RE = re.compile(r"^_meetperiode_(?P<ticket>[A-Z]+-\d+)_(?P<sensor>[A-Z0-9_]+?)_(?P<gemeente>[^_]+)\.parquet$")

# ---------------------------------------------------------------------------
# Thema: De Rode Ridder
# ---------------------------------------------------------------------------

SCHURKEN = [
    "Ahriman", "Alastor", "Ankou", "Arak", "Asmodon", "Astaroth", "Bahaal",
    "Balor", "Boggolt", "Cagliostro", "Dagon", "Demoniah", "Diabolos",
    "Doodgraver", "Draconis", "Draal", "Gorgontar", "Gruzal", "Hecate",
    "Iblis", "Ikar", "Kardan", "Knif", "Kronos", "Lucifer", "Marduk",
    "Mephisto", "Mordred", "Morgana", "Nergal", "Obscurion", "Qrandar",
    "Quasitor", "Sauron", "Sulphur", "Thanatos", "Toth", "Vargar", "Wargan",
    "Xanador", "Zardoz", "Zhar", "Zorak", "Gwion", "Lodogran", "Malfrat",
    "Tuan",
]
PLAATS_PREFIXEN = [
    "Zwart", "Doorn", "Nacht", "Ravenklauw", "Wolfs", "Bloed", "Schaduw",
    "IJzer", "Draken", "Grimoor", "Rots", "Storm", "Nevel", "Vuur", "Duister",
    "Grafsteen", "Ruwaard", "Helhoorn", "Wraak", "Verdoemenis",
]
PLAATS_SUFFIXEN = [
    "steen", "dal", "burcht", "hoven", "veld", "woud", "gracht", "donk",
    "berg", "hout", "poort", "wijk", "hoek", "beke", "dries", "gem",
    "zele", "kerke",
]
STRAAT_SUFFIXEN = ["straat", "laan", "weg", "dreef", "pad", "hof", "dries", "kaai", "wal"]
DOMEIN = "graalburcht.example"

# ---------------------------------------------------------------------------
# Deterministische hulpmiddelen
# ---------------------------------------------------------------------------


def stabiel(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().upper()


class UniekeGenerator:
    """Beeldt een genormaliseerde echte waarde af op een unieke fictieve waarde; bij een botsing
    opnieuw met een zout."""

    def __init__(self, fabriek):
        self.fabriek = fabriek
        self.afbeelding = {}
        self.gebruikt = set()

    def get(self, echt: str) -> str:
        sleutel = norm(echt)
        if sleutel in self.afbeelding:
            return self.afbeelding[sleutel]
        zout = 0
        while (kandidaat := self.fabriek(sleutel, zout)) in self.gebruikt:
            zout += 1
        self.gebruikt.add(kandidaat)
        self.afbeelding[sleutel] = kandidaat
        return kandidaat


def maak_plaats(sleutel, zout):
    h = stabiel(sleutel + f"#{zout}")
    return PLAATS_PREFIXEN[h % len(PLAATS_PREFIXEN)] + PLAATS_SUFFIXEN[(h // len(PLAATS_PREFIXEN)) % len(PLAATS_SUFFIXEN)]


def maak_straat(sleutel, zout):
    h = stabiel("straat#" + sleutel + f"#{zout}")
    return SCHURKEN[h % len(SCHURKEN)] + STRAAT_SUFFIXEN[(h // len(SCHURKEN)) % len(STRAAT_SUFFIXEN)]


def maak_postcode(sleutel, zout):
    return str(1000 + stabiel("postcode#" + sleutel + f"#{zout}") % 9000)


def maak_persoon(sleutel, zout):
    h = stabiel("persoon#" + sleutel + f"#{zout}")
    voornaam = SCHURKEN[h % len(SCHURKEN)]
    naam = SCHURKEN[(h // len(SCHURKEN)) % len(SCHURKEN)]
    if voornaam == naam:
        naam = SCHURKEN[(SCHURKEN.index(naam) + 1) % len(SCHURKEN)]
    return f"{voornaam}|{naam}"


gemeenten = UniekeGenerator(maak_plaats)
straten = UniekeGenerator(maak_straat)
postcodes = UniekeGenerator(maak_postcode)
personen = UniekeGenerator(maak_persoon)


def persoon(naam: str, voornaam: str) -> tuple[str, str]:
    if naam.strip() in ("", "//") and voornaam.strip() in ("", "//"):
        return naam, voornaam
    v, n = personen.get(f"{naam}|{voornaam}").split("|")
    return n, v


def email(adres: str) -> str:
    if not adres.strip():
        return adres
    v, n = personen.get("email#" + adres).split("|")
    return f"{v}.{n}@{DOMEIN}".lower()


# ---------------------------------------------------------------------------
# Bestanden
# ---------------------------------------------------------------------------


def pseudonimiseer_csv() -> str:
    tekst = CSV.read_text(encoding="utf-8")
    lezer = csv.DictReader(io.StringIO(tekst))
    uit = io.StringIO()
    schrijver = csv.DictWriter(uit, fieldnames=lezer.fieldnames, lineterminator="\n")
    schrijver.writeheader()
    for r in lezer:
        r["Custom field ((E-mail) Contactpersoon)"] = email(r["Custom field ((E-mail) Contactpersoon)"])
        r["Custom field (Naam)"], r["Custom field (Voornaam)"] = persoon(r["Custom field (Naam)"], r["Custom field (Voornaam)"])
        r["Custom field (Straat)"] = straten.get(r["Custom field (Straat)"])
        r["Custom field (Postcode)"] = postcodes.get(r["Custom field (Postcode)"])
        r["Custom field (Gemeente)"] = gemeenten.get(r["Custom field (Gemeente)"])
        schrijver.writerow(r)
    return uit.getvalue()


def parquetbestanden():
    for p in sorted(BRON.glob("_meetperiode_*.parquet")):
        m = PARQUET_RE.match(p.name)
        if not m:
            raise SystemExit(f"Onverwachte bestandsnaam: {p.name}")
        echt = m.group("gemeente")
        nep = gemeenten.get(echt)
        yield p, p.with_name(f"_meetperiode_{m.group('ticket')}_{m.group('sensor')}_{nep}.parquet"), echt, nep


def pseudonimiseer_parquet(pad: Path, nieuw: Path, echt: str, nep: str) -> None:
    tabel = pq.read_table(pad)
    i = tabel.schema.get_field_index("meetperiode")
    kolom = pc.replace_substring(tabel.column(i), pattern="_" + echt, replacement="_" + nep)
    tabel = tabel.set_column(i, tabel.schema.field(i), kolom)
    pq.write_table(tabel, nieuw, compression="snappy")
    if nieuw != pad:
        pad.unlink()


def main():
    csv_nieuw = pseudonimiseer_csv()
    parquets = list(parquetbestanden())
    rapport = {
        "gemeenten": len(gemeenten.afbeelding), "straten": len(straten.afbeelding),
        "postcodes": len(postcodes.afbeelding), "personen": len(personen.afbeelding),
        "parquet": [f"{p.name} → {n.name}" for p, n, _, _ in parquets],
    }
    if "--report-only" in sys.argv:
        # De afbeelding zelf (echt → fictief) gaat enkel naar het scherm, nooit naar een bestand.
        rapport["afbeelding"] = {"gemeenten": gemeenten.afbeelding, "straten": straten.afbeelding,
                                 "postcodes": postcodes.afbeelding, "personen": personen.afbeelding}
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
        return
    if "--apply" not in sys.argv:
        raise SystemExit(__doc__)
    CSV.write_text(csv_nieuw, encoding="utf-8")
    for p, n, echt, nep in parquets:
        pseudonimiseer_parquet(p, n, echt, nep)
    print(json.dumps(rapport, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
