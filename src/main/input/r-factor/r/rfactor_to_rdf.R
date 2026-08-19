# Voer uit vanuit src/main/input/r-factor/:
#   Rscript r/rfactor_to_rdf.R
# Of in RStudio:
#   setwd("src/main/input/r-factor"); source("r/rfactor_to_rdf.R")

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(jsonlite)
  library(lubridate)
})

# ─── Werkdirectory detecteren ─────────────────────────────────────────────────
args <- commandArgs(trailingOnly = FALSE)
script_file <- sub("--file=", "", args[grep("--file=", args)])
if (length(script_file) > 0) {
  rfactor_dir <- dirname(dirname(normalizePath(script_file)))
  setwd(rfactor_dir)
}

# ─── Inlezen ──────────────────────────────────────────────────────────────────
message("Inlezen CSV-bestanden ...")
stations    <- read_csv("stations_rfactor.csv",    show_col_types = FALSE)
view        <- read_csv("view_rfactor.csv",         show_col_types = FALSE)
jaarlijks   <- read_csv("jaarlijkse_rfactor.csv",   show_col_types = FALSE)
maandelijks <- read_csv("maandelijkse_rfactor.csv", show_col_types = FALSE)
perioden    <- read_csv("15-daagse_rfactor.csv",    show_col_types = FALSE)

beheerder_lu <- stations %>% select(station, beheerder)
jaarlijks    <- left_join(jaarlijks,   beheerder_lu, by = "station")
maandelijks  <- left_join(maandelijks, beheerder_lu, by = "station")
perioden     <- left_join(perioden,    beheerder_lu, by = "station")

# ─── Hulpfuncties ─────────────────────────────────────────────────────────────
clean    <- function(s) gsub("_", "-", s)
val_date <- function(d) list(`@value` = as.character(d), `@type` = "xsd:date")
val_dec  <- function(v) list(`@value` = as.character(round(v, 3)), `@type` = "xsd:decimal")

# time:Interval met benoemde IRIs — alle blank nodes zijn skoelm-IRIs
interval <- function(begin, end, id) list(
  `@id`               = paste0("ex:interval-", id),
  `@type`             = "time:Interval",
  `time:hasBeginning` = list(
    `@id`            = paste0("ex:instant-", id, "-begin"),
    `@type`          = "time:Instant",
    `time:inXSDDate` = val_date(begin)
  ),
  `time:hasEnd` = list(
    `@id`            = paste0("ex:instant-", id, "-end"),
    `@type`          = "time:Instant",
    `time:inXSDDate` = val_date(end)
  )
)

# qudt:QuantityValue met benoemde IRI
qty <- function(v, id) list(
  `@id`               = paste0("ex:result-", id),
  `@type`             = "qudt:QuantityValue",
  `qudt:numericValue` = val_dec(v),
  `qudt:hasUnit`      = list(`@id` = "ex:unit-rfactor")
)

# Datum begin/einde voor 15-daagse perioden (24 perioden per jaar, 2 per maand)
periode_interval <- function(jaar, p) {
  m <- ceiling(p / 2)
  if ((p %% 2) == 1) {
    list(begin = make_date(jaar, m, 1), end = make_date(jaar, m, 16))
  } else {
    list(begin = make_date(jaar, m, 16), end = make_date(jaar, m, 1) %m+% months(1))
  }
}

# ─── JSON-LD context ─────────────────────────────────────────────────────────
ctx <- list(
  sosa = "http://www.w3.org/ns/sosa/",
  time = "http://www.w3.org/2006/time#",
  qudt = "http://qudt.org/schema/qudt/",
  geo  = "http://www.opengis.net/ont/geosparql#",
  rdfs = "http://www.w3.org/2000/01/rdf-schema#",
  xsd  = "http://www.w3.org/2001/XMLSchema#",
  ex   = "https://example.org/rfactor/"
)

# ─── Gedeelde resources ───────────────────────────────────────────────────────
message("Gedeelde resources opbouwen ...")

gedeeld <- list(
  list(
    `@id`          = "ex:vlaanderen",
    `@type`        = "sosa:FeatureOfInterest",
    `rdfs:label`   = list(`@value` = "Vlaanderen", `@language` = "nl"),
    `rdfs:comment` = list(`@value` = "Studiegebied: Vlaamse regio, Belgie. Alle meetstations zijn ruimtelijke deelmonsters van dit studieobject.", `@language` = "nl")
  ),
  list(
    `@id`          = "ex:procedure-rfactor-kmi",
    `@type`        = "sosa:ObservingProcedure",
    `rdfs:label`   = list(`@value` = "KMI R-factor berekening", `@language` = "nl"),
    `rdfs:comment` = list(`@value` = "Berekening van de RUSLE R-factor via KMI-neerslagstations (pluviografen).", `@language` = "nl")
  ),
  list(
    `@id`          = "ex:procedure-rfactor-vmm",
    `@type`        = "sosa:ObservingProcedure",
    `rdfs:label`   = list(`@value` = "VMM R-factor berekening", `@language` = "nl"),
    `rdfs:comment` = list(`@value` = "Berekening van de RUSLE R-factor via VMM-hydrometriestations (telemetrische neerslagmeters).", `@language` = "nl")
  ),
  list(
    `@id`          = "ex:property-erosiviteit",
    `@type`        = "sosa:Property",
    `rdfs:label`   = list(`@value` = "Regenval-erosiviteit (R-factor)", `@language` = "nl"),
    `rdfs:comment` = list(`@value` = "RUSLE R-factor: erosieve kracht van neerslag, uitgedrukt in MJ mm/(ha h jaar).", `@language` = "nl")
  ),
  list(
    `@id`          = "ex:unit-rfactor",
    `@type`        = "qudt:Unit",
    `rdfs:label`   = list(`@value` = "MJ·mm/(ha·h·jaar)"),
    `rdfs:comment` = list(`@value` = "Eenheid van de RUSLE R-factor erosiviteitsindex (geen standaard QUDT-eenheid).", `@language` = "nl")
  ),
  list(
    `@id`          = "ex:departement-omgeving",
    `@type`        = "sosa:Platform",
    `rdfs:label`   = list(`@value` = "Departement Omgeving", `@language` = "nl"),
    `rdfs:comment` = list(`@value` = "Vlaamse overheidsdienst die de RUSLE R-factor centraal berekent op basis van de ruwe neerslagdata van het KMI- en VMM-meetnet (Vlaams Erosiemeetnet).", `@language` = "nl"),
    `sosa:hosts`   = list(`@id` = "ex:sensor-rfactor")
  ),
  list(
    `@id`   = "ex:sensor-rfactor",
    `@type` = "sosa:Sensor",
    `rdfs:label`      = list(`@value` = "Centrale R-factor berekeningsketen", `@language` = "nl"),
    `sosa:isHostedBy` = list(`@id` = "ex:departement-omgeving"),
    `sosa:implements` = list(list(`@id` = "ex:procedure-rfactor-kmi"), list(`@id` = "ex:procedure-rfactor-vmm")),
    `sosa:observes`   = list(`@id` = "ex:property-erosiviteit")
  )
)

# ─── Platforms & sensoren ────────────────────────────────────────────────────
message("Platforms en sensoren opbouwen ...")

view_lu <- view %>% select(station, meting_van, meting_tot, aantal_gevalideerde_jaren)

infra <- lapply(seq_len(nrow(stations)), function(i) {
  s  <- stations[i, ]
  sc <- clean(s$station)
  v  <- view_lu[view_lu$station == s$station, ]

  comment <- if (nrow(v) > 0)
    sprintf("%s-station %s te %s. Meetperiode: %s–%s (%s gevalideerde jaren).",
            s$beheerder, s$station, s$locatie, v$meting_van, v$meting_tot, v$aantal_gevalideerde_jaren)
  else
    sprintf("%s-station %s te %s.", s$beheerder, s$station, s$locatie)

  list(
    `@id`   = paste0("ex:", sc),
    `@type` = c("sosa:Platform", "sosa:FeatureOfInterest", "sosa:SpatialSample"),
    `rdfs:label`   = list(`@value` = s$locatie, `@language` = "nl"),
    `rdfs:comment` = list(`@value` = comment, `@language` = "nl"),
    `geo:hasGeometry` = list(
      `@id`     = paste0("ex:geom-", sc),
      `@type`   = "geo:Geometry",
      `geo:asWKT` = list(
        `@value` = sprintf("SRID=31370;POINT(%s %s)", s$x, s$y),
        `@type`  = "geo:wktLiteral"
      )
    ),
    `sosa:isSampleOf`            = list(`@id` = "ex:vlaanderen"),
    `sosa:isFeatureOfInterestOf` = list(`@id` = paste0("ex:collectie-", sc, "-jaarlijks"))
  )
})

# ─── Jaarlijkse observaties & collecties ─────────────────────────────────────
message(sprintf("Jaarlijkse observaties opbouwen (%d records) ...", nrow(jaarlijks)))

obs_jaar <- lapply(seq_len(nrow(jaarlijks)), function(i) {
  r    <- jaarlijks[i, ]
  sc   <- clean(r$station)
  oid  <- paste0(sc, "-jaar-", r$jaar)
  list(
    `@id`   = paste0("ex:obs-", sc, "-", r$jaar),
    `@type` = "sosa:Observation",
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:phenomenonTime`       = interval(make_date(r$jaar, 1, 1), make_date(r$jaar + 1, 1, 1), oid),
    `sosa:hasResult`            = qty(r$erosiviteit, oid),
    `sosa:isMemberOf`           = list(`@id` = paste0("ex:collectie-", sc, "-jaarlijks"))
  )
})

jaarlijks_g <- jaarlijks %>%
  group_by(station, beheerder) %>%
  summarise(jaren = list(jaar), .groups = "drop")

coll_jaar <- lapply(seq_len(nrow(jaarlijks_g)), function(i) {
  r  <- jaarlijks_g[i, ]
  sc <- clean(r$station)
  list(
    `@id`   = paste0("ex:collectie-", sc, "-jaarlijks"),
    `@type` = "sosa:ObservationCollection",
    `rdfs:label`                = list(`@value` = sprintf("Jaarlijkse erosiviteitscollectie %s", r$station), `@language` = "nl"),
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:hasMember`            = lapply(r$jaren[[1]], function(j)
      list(`@id` = paste0("ex:obs-", sc, "-", j)))
  )
})

# ─── Maandelijkse observaties & collecties ────────────────────────────────────
message(sprintf("Maandelijkse observaties opbouwen (%d records) ...", nrow(maandelijks)))

obs_maand <- lapply(seq_len(nrow(maandelijks)), function(i) {
  r     <- maandelijks[i, ]
  sc    <- clean(r$station)
  oid   <- paste0(sc, "-maand-", r$jaar, "-m", sprintf("%02d", r$maand_id))
  begin <- make_date(r$jaar, r$maand_id, 1)
  end   <- begin %m+% months(1)
  list(
    `@id`   = paste0("ex:obs-", sc, "-", r$jaar, "-m", sprintf("%02d", r$maand_id)),
    `@type` = "sosa:Observation",
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:phenomenonTime`       = interval(begin, end, oid),
    `sosa:hasResult`            = qty(r$erosiviteit, oid),
    `sosa:isMemberOf`           = list(`@id` = paste0("ex:collectie-", sc, "-", r$jaar, "-maandelijks"))
  )
})

maand_g <- maandelijks %>%
  group_by(station, jaar, beheerder) %>%
  summarise(maanden = list(maand_id), .groups = "drop")

coll_maand <- lapply(seq_len(nrow(maand_g)), function(i) {
  r  <- maand_g[i, ]
  sc <- clean(r$station)
  list(
    `@id`   = paste0("ex:collectie-", sc, "-", r$jaar, "-maandelijks"),
    `@type` = "sosa:ObservationCollection",
    `rdfs:label`                = list(`@value` = sprintf("Maandelijkse erosiviteitscollectie %s, %d", r$station, r$jaar), `@language` = "nl"),
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:hasMember`            = lapply(r$maanden[[1]], function(m)
      list(`@id` = paste0("ex:obs-", sc, "-", r$jaar, "-m", sprintf("%02d", m))))
  )
})

# ─── 15-daagse observaties & collecties ──────────────────────────────────────
message(sprintf("15-daagse observaties opbouwen (%d records) ...", nrow(perioden)))

obs_15d <- lapply(seq_len(nrow(perioden)), function(i) {
  r     <- perioden[i, ]
  sc    <- clean(r$station)
  oid   <- paste0(sc, "-15d-", r$jaar, "-p", sprintf("%02d", r$periode))
  dates <- periode_interval(r$jaar, r$periode)
  list(
    `@id`   = paste0("ex:obs-", sc, "-", r$jaar, "-p", sprintf("%02d", r$periode)),
    `@type` = "sosa:Observation",
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:phenomenonTime`       = interval(dates$begin, dates$end, oid),
    `sosa:hasResult`            = qty(r$erosiviteit, oid),
    `sosa:isMemberOf`           = list(`@id` = paste0("ex:collectie-", sc, "-", r$jaar, "-15daags"))
  )
})

perioden_g <- perioden %>%
  group_by(station, jaar, beheerder) %>%
  summarise(periodes = list(periode), .groups = "drop")

coll_15d <- lapply(seq_len(nrow(perioden_g)), function(i) {
  r  <- perioden_g[i, ]
  sc <- clean(r$station)
  list(
    `@id`   = paste0("ex:collectie-", sc, "-", r$jaar, "-15daags"),
    `@type` = "sosa:ObservationCollection",
    `rdfs:label`                = list(`@value` = sprintf("15-daagse erosiviteitscollectie %s, %d", r$station, r$jaar), `@language` = "nl"),
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", tolower(r$beheerder))),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:hasMember`            = lapply(r$periodes[[1]], function(p)
      list(`@id` = paste0("ex:obs-", sc, "-", r$jaar, "-p", sprintf("%02d", p))))
  )
})

# ─── Gemiddelde-observaties (afgeleide, R13) ─────────────────────────────────
message("Gemiddelde-observaties opbouwen (afgeleide R13) ...")

obs_gem <- lapply(seq_len(nrow(view)), function(i) {
  v   <- view[i, ]
  sc  <- clean(v$station)
  oid <- paste0(sc, "-gemiddelde")
  bh  <- tolower(v$beheerder)
  jaren_st <- jaarlijks$jaar[jaarlijks$station == v$station]
  input_waarden <- lapply(jaren_st, function(j)
    list(`@id` = paste0("ex:result-", sc, "-jaar-", j)))
  list(
    `@id`   = paste0("ex:obs-", oid),
    `@type` = "sosa:Observation",
    `rdfs:label`                = list(`@value` = sprintf("Gemiddelde jaarlijkse erosiviteit %s (%s–%s)", v$station, v$meting_van, v$meting_tot), `@language` = "nl"),
    `sosa:madeBySensor`         = list(`@id` = "ex:sensor-rfactor"),
    `sosa:usedProcedure`        = list(`@id` = paste0("ex:procedure-rfactor-", bh)),
    `sosa:hasFeatureOfInterest` = list(`@id` = paste0("ex:", sc)),
    `sosa:observedProperty`     = list(`@id` = "ex:property-erosiviteit"),
    `sosa:phenomenonTime`       = interval(
      make_date(v$meting_van, 1, 1),
      make_date(v$meting_tot + 1, 1, 1),
      oid
    ),
    `sosa:hasInputValue`      = input_waarden,
    `sosa:relatedObservation` = list(`@id` = paste0("ex:collectie-", sc, "-jaarlijks")),
    `sosa:hasResult`          = qty(v$gemiddelde_waarde, oid)
  )
})

# ─── Samenvoegen & serialiseren ───────────────────────────────────────────────
graph <- c(gedeeld, infra, coll_jaar, obs_jaar, coll_maand, obs_maand, coll_15d, obs_15d, obs_gem)
jsonld <- list(`@context` = ctx, `@graph` = graph)

message(sprintf("Schrijven rfactor.jsonld (%d resources) ...", length(graph)))
write_json(jsonld, "rfactor.jsonld", auto_unbox = TRUE, pretty = FALSE)

# ─── Volledige dataset → rfactor.trig (uitgesloten van mvn-validatie) ─────────
message("Converteren naar rfactor.trig (volledige dataset, ~44 MB) ...")
ret <- system("riot --output=turtle rfactor.jsonld > rfactor.trig")
if (ret != 0) stop("riot-conversie (trig) mislukt.")
message(sprintf("rfactor.trig aangemaakt (%.1f MB).", file.size("rfactor.trig") / 1e6))

# ─── Validatie-subset → rfactor.ttl (1 station: KMI_6408) ────────────────────
# Bevat alle drie aggregatieniveaus + gemiddelde voor KMI_6408.
# Dit bestand wordt wél meegenomen in mvn compile exec:java.
VALIDATIE_STATION <- "KMI-6408"

gedeeld_ids <- c("ex:vlaanderen", "ex:procedure-rfactor-kmi", "ex:procedure-rfactor-vmm",
                 "ex:property-erosiviteit", "ex:unit-rfactor",
                 "ex:departement-omgeving", "ex:sensor-rfactor")

graph_validatie <- Filter(function(x) {
  id <- x[["@id"]]
  if (is.null(id)) return(FALSE)
  id %in% gedeeld_ids ||
    grepl(paste0("^ex:(", VALIDATIE_STATION,
                 "|geom-", VALIDATIE_STATION,
                 "|collectie-", VALIDATIE_STATION,
                 "|obs-", VALIDATIE_STATION,
                 "|interval-", VALIDATIE_STATION,
                 "|instant-", VALIDATIE_STATION,
                 "|result-", VALIDATIE_STATION, ")"),
          id)
}, graph)

message(sprintf("Validatie-subset: %d resources (station %s).", length(graph_validatie), VALIDATIE_STATION))
jsonld_val <- list(`@context` = ctx, `@graph` = graph_validatie)
write_json(jsonld_val, "rfactor_validatie.jsonld", auto_unbox = TRUE, pretty = FALSE)

ret <- system("riot --output=turtle rfactor_validatie.jsonld > rfactor.ttl")
if (ret != 0) stop("riot-conversie (ttl validatie) mislukt.")
message(sprintf("rfactor.ttl aangemaakt (%.0f KB, validatie-subset).",
                file.size("rfactor.ttl") / 1e3))
file.remove("rfactor_validatie.jsonld")
