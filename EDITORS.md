# OSLOthema-myTheme

This branch should be used to make the data standard available on the [standards registry of Flanders](https://data.vlaanderen.be/standaarden/).

## Structure of this repository

This repository contains four folders to store data standard related information.

### Charter

This folder should contain the OSLO charter. Accepted file formats are Word (`.docx`) or PDF (`.pdf`).

### Descriptions

For each data standard a short description is required that will be displayed on the detail page on the standards registry. Multiple files (descriptions) are allowed, e.g. one for the application profile and one for the vocabulary. The file format must be Markdown (`.md`).

### Presentations

Presentations given by the OSLO Editors during one of the workshop can be stored in this folder. Accepted file format are Powerpoint (`.pptx`) and PDF (`.pdf`). The formatting of the file name should be: 'YYYYMMDD_TypeWorkshopX_Slides_OSLOnameoftrack'

### Reports

After each workshop a report of that workshop is made by the OSLO Editors, which can be stored in this folder. Accepted file format are Word (`.docx`) and PDF (`.pdf`). The formatting of the file name should be: 'YYYYMMDD_TypeWorkshopX_Report_OSLOnameoftrack'

### ap-or-voc-config.json

This is the file that must be used to configure the standard for publication on the standards registry. If the OSLO Editor wants to publish the application profile and vocabulary on the standards registry separately, then **two** configuration files must be created. Don't forget to change the name of the file so it is clear which standard this refers to.

## Content of the configuration file

### `title`

This is the name of the data standard, e.g. _Applicatieprofiel LDES_ or _Vocabularium Persoon_. The format of the title should always be 'TypeOfSpecification DomainOfStandard'.

### `category`

The category of the data standard. Allowed values are:

- https://data.vlaanderen.be/id/concept/StandaardType/Applicatieprofiel
- https://data.vlaanderen.be/id/concept/StandaardType/Vocabularium
- https://data.vlaanderen.be/id/concept/StandaardType/Implementatiemodel
- https://data.vlaanderen.be/id/concept/StandaardType/TechnischeStandaard
- https://data.vlaanderen.be/id/concept/StandaardType/Interoperabiliteit

### `usage`

Is the usage of the data standard mandatory or recommended? Allowed values are:

- https://data.vlaanderen.be/id/concept/StandaardGebruik/Aanbevolen
- https://data.vlaanderen.be/id/concept/StandaardGebruik/Verplicht
- https://data.vlaanderen.be/id/concept/StandaardGebruik/PasToeOfLegUit

### `status`

Different stages of the data standard lifecycle:

- https://data.vlaanderen.be/id/concept/StandaardStatus/OntwerpStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/KandidaatStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/ErkendeStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/VerouderdeStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/VervangenStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/HerroepenStandaard
- https://data.vlaanderen.be/id/concept/StandaardStatus/NotaWerkgroep

### `responsibleOrganisation`

The name of the organisation(s) that is responsible for the data standard.

#### `name`

The name of the organisation that is responsible for the data standard

#### `resourceReference`

The uri of the organisation that is responsible for the data standard.

To construct the URI of the organisation, the [Wegwijs application](https://wegwijs.vlaanderen.be/#/organisations) can be used to find the OVO-code (identifier of an organisation). The URI has the following structure `https://data.vlaanderen.be/id/organisatie/{OVO-code}`. It is mandatory to use the OVO code of an organisation when available.

### `publicationDate`

Date on which the most recent version of the standard was published. Only YYYY-MM-DD is an accepted format.

### `descriptionFileName`

The name of the Markdown file (stored in the `descriptions` folder) that contains the description to be displayed on the standards registry.

### `specificationDocuments`

Links to the application profile(s) or vocabulary. This **must** always be an array of objects with the properties `name` and `uri`.

#### Example

```json
"specificationDocuments": [
    {
        "name": "Applicatieprofiel LDES",
        "resourceReference": "https://data.vlaanderen.be/doc/applicatieprofiel/ldes"
    }
]
```

### `documentation`

Additional documentation to be displayed on the detail page of the data standard, e.g. a mapping described in an Excel file or link to external specification.

This **must** always be an array of objects containing the properties `name` and `resourceReference`. The `resourceReference`property can be used to reference a URI such as `https://example.org/externalSpec` but it can also be a document that was stored in the `documentation` folder. In that case you can write the name of the file.

#### Example

```json
"documentation": [
    {
        "name": "Voorbeeld van een mapping",
        "resourceReference": "mapping-voorbeeld.xlsx"
    },
    {
        "name": "Link naar externe spec",
        "resourceReference": "https://example.org/externalSpec"
    }
]
```

### `charter`

The OSLO charter that will be displayed on the detail page of the data standard. This **must** always be an object containing the properties `name` and `resourceReference`. The `resourceReference`property can be used to reference a URI such as `https://example.org/externalSpec` but it can also be a document that was stored in the `charter` folder. In that case you can write the name of the file. It should use the following format: 'OSLO Charter TrackX'. OSLO Charters are linked to OSLO tracks, not specific standards. The same charter can be reused and found across multiple specifications. 

#### Example

```json
"charter": {
    "name": "OSLO Charter TrackX",
    "resourceReference": "oslo_charter_trackX.docx"
}
```

### `reports`

Reports made of the workshop to be displayed on the detail page of the data standard.

This **must** always be an array of objects containing the properties `name` and `resourceReference`. The `resourceReference`property can be used to reference a URI such as `https://example.org/externalSpec` but it can also be a document that was stored in the `reports` folder. In that case you can write the name of the file.

#### Example

```json
"reports": [
    {
        "name": "Verslag Werkgroep 1 - DD month YYYY",
        "resourceReference": "YYYYMMDD_ThematicWorkshop1_Report_OSLOtrackX.pdf"
    }
]
```

### `presentations`

Presentations that were used during the workshop and must be displayed on the detail page of the data standard.

This **must** always be an array of objects containing the properties `name` and `resourceReference`. The `resourceReference`property can be used to reference a URI such as `https://example.org/externalSpec` but it can also be a document that was stored in the `presentations` folder. In that case you can write the name of the file

#### Example

```json
"presentations": [
    {
        "name": "Presentatie Thematische Werkgroep 1 - DD month YYYY",
        "resourceReference": "YYYYMMDD_ThematicWorkshop1_Slides_OSLOtrackX.pptx"
    },
    {
        "name": "Presentatie Thematische Werkgroep 2 - DD month YYYY",
        "resourceReference": "YYYYMMDD_ThematicWorkshop2_Slides_OSLOtrackX.pptx"
    }
]
```

### `dateOfRegistration`

The date on which the data standard was announced on the working group 'Data Standards'.

### `dateOfAcknowledgementByWorkingGroup`

The date on which the data standard was accepted as an acknowledged standard by the working group 'Data standards'.

### `dateOfAcknowledgementBySteeringCommittee`

The date on which the data standard was accepted as an acknowledged standard by the steering committee 'Flemish Information and ICT policy'.

### `datePublicReviewStart`

The date on which the public review of the data standard started.

### `datePublicReviewEnd`

The date on which the public review of the data standard ended.

### `endOfPublicationDate`

The date on which the data standard is no longer valid and shouldn't be used anymore.

### `functionalScope`

The functional scope of the data standard.
