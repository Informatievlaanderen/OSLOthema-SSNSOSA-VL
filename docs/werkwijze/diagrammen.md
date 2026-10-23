# Diagrammen

Elk model heeft een Mermaid-diagram (`<naam>.mmd`). Eén kleurconventie voor alle voorbeelden maakt
dat een lezer in elk diagram meteen ziet wat infrastructuur, uitvoering en waarde is.

## Kleuren

| Element | Kleur | Gebruik |
|---|---|---|
| subgraph INFRASTRUCTUUR | <span class="swatch" style="background:#b0d9e7"></span> `#b0d9e7` | |
| platform, systeem, sensor, studieobject | <span class="swatch" style="background:#60c4e4"></span> `#60c4e4` | tekst zwart |
| subgraph PROCEDURE / PLANNING | <span class="swatch" style="background:#b8a2d4"></span> `#b8a2d4` | |
| `p-plan:Plan`, `p-plan:Step` | <span class="swatch" style="background:#7f59ae"></span> `#7f59ae` | tekst wit |
| `sosa:Procedure` | <span class="swatch" style="background:#c6a0f5"></span> `#c6a0f5` | |
| eigenschap, variabele | <span class="swatch" style="background:#fe7130"></span> `#fe7130` | |
| subgraph WAARNEMING / EXECUTION | <span class="swatch" style="background:#e7a3be"></span> `#e7a3be` | |
| waarneming, actuatie, activiteit | <span class="swatch" style="background:#e54b89"></span> `#e54b89` | tekst wit |
| resultaat, entiteit, tijdstip | <span class="swatch" style="background:#f8b622"></span> `#f8b622` | |
| subgraph DERIVATION | <span class="swatch" style="background:#f8e1ad"></span> `#f8e1ad` | |

Rand overal `#2E5C8A`. Elke node krijgt een eigen `style`-regel, na de subgraphs.

## Opbouw

**Plat model** (`flowchart LR`), drie naast elkaar liggende subgraphs:

```text
subgraph PROC["PROCEDURE"] … end
subgraph INFRA["INFRASTRUCTUUR"] … end
subgraph WAAR["WAARNEMING"] … end
```

**Drielaags model** (`flowchart RL`), met een geneste DERIVATION:

```text
subgraph PLANNING["PLANNING"] … end
subgraph DEPLOYMENT["DEPLOYMENT"] … end
subgraph EXECUTION["EXECUTION"]
    subgraph DERIVATION["DERIVATION"] … end
end
```

Relaties die subgraphs kruisen, komen na alle subgraphdefinities.

## Labels

De korte naam van de eigenschap: `-->|sosa:hosts|`, `-->|correspondsToStep|`; een stippellijn voor
volgorde: `-.->|isPrecededBy|`.

## Samenhang met de Turtle

Elke IRI in het diagram staat ook in de Turtle. Een **vergelijkingsdiagram**
(`<naam>_vergelijking.mmd`) zet twee modellen naast elkaar, gericht op wat verschilt: vóór en na
een herziening, of een hoofdmodel en zijn alternatief.

## Een voorbeeld

```mermaid
--8<-- "src/main/input/erosiepoel/erosiepoel.mmd"
```

*Het diagram van de [erosiepoel](../casussen/erosiepoel.md), rechtstreeks uit de repository.*
