---
description: Nieuw SSN/SOSA Datavoorbeeld aanmaken
allowed-tools: Skill, mcp__ld-vocab__lookup_term, mcp__ld-vocab__search_terms, mcp__ld-vocab__validate_file
---

# Nieuw SSN/SOSA Datavoorbeeld aanmaken

Volg de skill **`oslo-ld:new-example`** (plugin `oslo-ld`, kit in de submodule `oslo-ld-kit/`). Is de plugin
niet geïnstalleerd, lees en volg dan `oslo-ld-kit/skills/new-example/SKILL.md`. Kiest de
gebruiker bij vraag 4 een herziening of een alternatief, volg dan `oslo-ld:revise-mapping`
respectievelijk `oslo-ld:alternative-mapping` (`oslo-ld-kit/skills/…/SKILL.md`).

Gebruik het **projectprofiel** uit `CLAUDE.md` §2 en de bestandsset uit §4:

- Map: `src/main/input/<domein>/`; voor een alternatief `src/main/input/<bestaand-domein>/alternatief/`.
- Alle documenten in het **Nederlands**: `README.md`, `bespreking.md` (Nederlandse sectietitels,
  `## 1. Wat stelt dit voorbeeld voor?` …), `opdracht.md`; bij een herziening
  `<naam>_herzien.ttl`, `<naam>_vergelijking.mmd` en de README-sectie *Verbeterpunten*.
- Stel de vragen van stap 1 in het Nederlands.
- Bronbestanden in `source/`, Turtle als `source/<naam>.trig`.
- Tijdzone zonder bronvermelding: `Europe/Brussels` (R12).
- Eenhedenregister bij vraag 6: CSOR (`csor-eenheid:`).
- Valideren met `mcp__ld-vocab__validate_file`; de pipeline (`mvn compile exec:java`) enkel als
  de output in `src/main/output/` nodig is.

Schrijf het eindrapport van stap 4 in het Nederlands.
