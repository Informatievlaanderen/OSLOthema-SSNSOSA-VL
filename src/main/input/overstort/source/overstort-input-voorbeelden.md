---
layout: default
title: Input data
parent: Aquafin
nav_order: 1
---

Onderstaande inputdata is afkomstig van 1600 overstortsensoren verspreid over Vlaanderen. Deze sensoren meten o.a. de periode waarin er sprake is van overstort. 
Een overstort is een kunstwerk met als doel het afvoeren van (pieken in) overtollig rioolwater vanuit de gemengde riolering naar het oppervlaktewater.
Dagelijks worden deze metingen doorgestuurd naar het dataplatform van Aquafin en wordt alle data verzameld in het datalake in Delta Parquet-files. 



# Data voorbeeld Overstortsensor Metadata 

| id |  P2050378 |
| device_type |  Overstortsensor |
| name |  Overstortmeter Ijinus US LTE |
| owner |  Aquafin |
| brand |  IJINUS |
| supplier |  ELSCOLAB |
| serial_number |  IJA0102-00004425 |
| device_state |  Actief |
| lat_WGS84 |  50.948995878 |
| long_WGS84 |  5.298607495000001 | 
| lat_Lambert72 |  193183.8663904309 | 
| long_Lambert72 |  235956.9331605651 | 
| measurement_location | P_000000217952 |
| load_timestamp_utc |  2025-02-16T22:01:04.229Z |
| change_timestamp_utc  |  2024-12-29T05:52:09.343Z |
| quality_label  |  0  |
| scd_update_timestamp  |  2025-02-14T08:46:50.202Z |



# Data voorbeeld Overstort Event 

| type |  event |
| start_timestamp |  2025-02-18T08:31:00.000Z |
| end_timestamp |  2025-02-18T08:41:00.000Z |
| modifiedAt |  2025-02-18T10:21:17.979Z | 
| measurement_location | P_000000181521 | 
| status |  InWerking | 
| is_observed_with |  P1037143 |  
| end_timestamp_known  |  true |
| sent_to_evh  |  false |
