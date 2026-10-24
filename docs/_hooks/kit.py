"""MkDocs-hook: haalt de normatieve teksten uit de kit (oslo-ld-kit/guide) en controleert de dekking.

De regels (R1-R18) en de patronen staan één keer, in het Engels, in de git-subtree
`oslo-ld-kit/`. Dit referentiewerk is de Nederlandse, didactische laag erbovenop. De hook:

1. schrijft elke regel- en patroonsectie van de gids naar `.cache/kit/<id>.md`, met de relatieve
   links omgezet naar GitHub, zodat een pagina ze met `--8<-- "kit/R3.md"` kan insluiten;
2. controleert dat elke regel en elk patroon van de kit een pagina heeft, en omgekeerd. Een nieuwe
   regel in de kit valt zo op als ontbrekend hoofdstuk (een fout in `mkdocs build --strict`).
"""

import json
import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.kit")

ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / "oslo-ld-kit" / "guide"
CACHE = ROOT / ".cache" / "kit"
KIT_URL = "https://github.com/milieuinfo/oslo-ld-kit/blob/main"

# patroontitel in patterns.md -> pagina in docs/patronen/
PATTERNS = {
    "Emission as feature of interest": "emissie",
    "Stimulus": "stimulus",
    "Sample with ultimate feature of interest": "monster",
    "Spatial sample": "ruimtelijk-monster",
    "Derived observation": "afgeleide-waarneming",
    "Reporting limit": "rapportagegrens",
}


def _sections(text):
    """Geeft (titel, inhoud) per sectie van niveau 2."""
    parts = re.split(r"(?m)^## ", text)
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        yield title.strip(), body.strip() + "\n"


def _absolute_links(body):
    """Relatieve links in de gids wijzen naar bestanden van de kit; maak ze absoluut."""

    def fix(match):
        label, target = match.group(1), match.group(2)
        if re.match(r"^[a-z]+:|^#", target):
            return match.group(0)
        path = target if target.startswith("../") else "guide/" + target
        path = path.replace("guide/../", "")
        return f"[{label}]({KIT_URL}/{path})"

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", fix, body)


def _kit_version():
    try:
        data = json.loads((ROOT / ".claude" / "skills" / ".oslo-ld-kit.json").read_text())
        return data.get("kit-version", "?")
    except (OSError, ValueError):
        return "?"


def on_config(config):
    CACHE.mkdir(parents=True, exist_ok=True)
    rules, patterns = set(), set()
    for md in sorted(GUIDE.glob("*.md")):
        for title, body in _sections(md.read_text(encoding="utf-8")):
            rule = re.match(r"R(\d+) — ", title)
            if rule:
                rid = f"R{int(rule.group(1))}"
                rules.add(rid)
                source = f"{KIT_URL}/guide/{md.name}"
                out = f"*{title}* — uit [`guide/{md.name}`]({source}), kit {_kit_version()}\n\n"
                (CACHE / f"{rid}.md").write_text(out + _absolute_links(body), encoding="utf-8")
            elif md.name == "patterns.md" and title in PATTERNS:
                patterns.add(PATTERNS[title])
                out = f"*{title}* — uit [`guide/patterns.md`]({KIT_URL}/guide/patterns.md)\n\n"
                (CACHE / f"patroon-{PATTERNS[title]}.md").write_text(
                    out + _absolute_links(body), encoding="utf-8")
    (CACHE / "versie.md").write_text(_kit_version() + "\n", encoding="utf-8")

    docs = Path(config["docs_dir"])
    pages = {f"R{int(p.stem[1:])}" for p in (docs / "regels").glob("r[0-9]*.md")}
    for rid in sorted(rules - pages, key=lambda r: int(r[1:])):
        log.error("Regel %s staat in de kit maar heeft geen pagina docs/regels/r%02d.md",
                  rid, int(rid[1:]))
    for rid in sorted(pages - rules, key=lambda r: int(r[1:])):
        log.error("Pagina voor %s, maar de kit kent die regel niet (meer)", rid)
    known = {p.stem for p in (docs / "patronen").glob("*.md")} - {"index"}
    for title, slug in PATTERNS.items():
        if slug not in known:
            log.error("Patroon '%s' heeft geen pagina docs/patronen/%s.md", title, slug)
    text = (GUIDE / "patterns.md").read_text(encoding="utf-8")
    for title, _ in _sections(text):
        if title not in PATTERNS:
            log.error("Nieuw patroon in de kit zonder pagina: '%s' (voeg toe aan PATTERNS)", title)
    return config
