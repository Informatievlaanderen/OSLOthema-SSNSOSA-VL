-- SSN/SOSA Plat Model — SQL schema
-- Ontologie: https://data.vlaanderen.be/ns/ssnsosa#
-- Gebaseerd op: src/main/input/r-factor/rfactor.ttl
-- ODDToolkit-compatibel: COMMENT ON TABLE/COLUMN bevat OWL-URI als mapping-metadata.
--
-- Tabellenstructuur:
--   REGULAR (9): meetstation, studiegebied, sensor, procedure,
--                eigenschap, eenheid, observatie_collectie,
--                resultaat, observatie
--   JOIN    (1): observatie_collectie_lid  (sosa:hasMember, M:N)
--
-- Geometrie: geom_wkt VARCHAR — WKT-literal conform geo:asWKT.
--   Bij PostGIS-ingestie omzetten: ST_GeomFromText(geom_wkt, 31370).
-- Tijdskolommen: DATE voor begin/eind (time:inXSDDate conform rfactor).
--   Gebruik TIMESTAMP WITH TIME ZONE bij TIMESTAMP-precisie nodig.
-- Foreign keys: aan het einde als ALTER TABLE statements.

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#StudieGebied
CREATE TABLE studiegebied (
  uri          VARCHAR,
  label        VARCHAR,
  beschrijving VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE studiegebied IS 'http://www.w3.org/ns/sosa/FeatureOfInterest';
COMMENT ON COLUMN studiegebied.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN studiegebied.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN studiegebied.beschrijving IS 'http://www.w3.org/2000/01/rdf-schema#comment';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#MeetStation
CREATE TABLE meetstation (
  uri          VARCHAR,
  label        VARCHAR,
  beschrijving VARCHAR,
  geom_wkt     VARCHAR,
  -- Foreign key referencing studiegebied(uri)
  sample_van   VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE meetstation IS 'http://www.w3.org/ns/sosa/Platform';
COMMENT ON COLUMN meetstation.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN meetstation.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN meetstation.beschrijving IS 'http://www.w3.org/2000/01/rdf-schema#comment';
COMMENT ON COLUMN meetstation.geom_wkt IS 'http://www.opengis.net/ont/geosparql#asWKT';
COMMENT ON COLUMN meetstation.sample_van IS 'http://www.w3.org/ns/sosa/isSampleOf';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#MeetProcedure
CREATE TABLE procedure (
  uri          VARCHAR,
  label        VARCHAR,
  beschrijving VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE procedure IS 'http://www.w3.org/ns/sosa/ObservingProcedure';
COMMENT ON COLUMN procedure.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN procedure.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN procedure.beschrijving IS 'http://www.w3.org/2000/01/rdf-schema#comment';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#ObserveerdeEigenschap
CREATE TABLE eigenschap (
  uri          VARCHAR,
  label        VARCHAR,
  beschrijving VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE eigenschap IS 'http://www.w3.org/ns/sosa/Property';
COMMENT ON COLUMN eigenschap.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN eigenschap.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN eigenschap.beschrijving IS 'http://www.w3.org/2000/01/rdf-schema#comment';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#Eenheid
CREATE TABLE eenheid (
  uri          VARCHAR,
  label        VARCHAR,
  beschrijving VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE eenheid IS 'http://qudt.org/schema/qudt/Unit';
COMMENT ON COLUMN eenheid.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN eenheid.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN eenheid.beschrijving IS 'http://www.w3.org/2000/01/rdf-schema#comment';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#Sensor
CREATE TABLE sensor (
  uri          VARCHAR,
  label        VARCHAR,
  -- Foreign key referencing meetstation(uri)
  host         VARCHAR,
  -- Foreign key referencing procedure(uri)
  implementeert VARCHAR,
  -- Foreign key referencing eigenschap(uri)
  observeert   VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE sensor IS 'http://www.w3.org/ns/sosa/Sensor';
COMMENT ON COLUMN sensor.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN sensor.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN sensor.host IS 'http://www.w3.org/ns/sosa/isHostedBy';
COMMENT ON COLUMN sensor.implementeert IS 'http://www.w3.org/ns/sosa/implements';
COMMENT ON COLUMN sensor.observeert IS 'http://www.w3.org/ns/sosa/observes';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#ObservatieCollectie
CREATE TABLE observatie_collectie (
  uri           VARCHAR,
  label         VARCHAR,
  -- Foreign key referencing meetstation(uri)
  foi_uri       VARCHAR,
  -- Foreign key referencing sensor(uri)
  sensor_uri    VARCHAR,
  -- Foreign key referencing procedure(uri)
  procedure_uri VARCHAR,
  -- Foreign key referencing eigenschap(uri)
  eigenschap_uri VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE observatie_collectie IS 'http://www.w3.org/ns/sosa/ObservationCollection';
COMMENT ON COLUMN observatie_collectie.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN observatie_collectie.label IS 'http://www.w3.org/2000/01/rdf-schema#label';
COMMENT ON COLUMN observatie_collectie.foi_uri IS 'http://www.w3.org/ns/sosa/hasFeatureOfInterest';
COMMENT ON COLUMN observatie_collectie.sensor_uri IS 'http://www.w3.org/ns/sosa/madeBySensor';
COMMENT ON COLUMN observatie_collectie.procedure_uri IS 'http://www.w3.org/ns/sosa/usedProcedure';
COMMENT ON COLUMN observatie_collectie.eigenschap_uri IS 'http://www.w3.org/ns/sosa/observedProperty';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#QuantitatieveWaarde
CREATE TABLE resultaat (
  uri         VARCHAR,
  waarde      DECIMAL,
  -- Foreign key referencing eenheid(uri)
  eenheid_uri VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE resultaat IS 'http://qudt.org/schema/qudt/QuantityValue';
COMMENT ON COLUMN resultaat.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN resultaat.waarde IS 'http://qudt.org/schema/qudt/numericValue';
COMMENT ON COLUMN resultaat.eenheid_uri IS 'http://qudt.org/schema/qudt/hasUnit';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#Observatie
CREATE TABLE observatie (
  uri            VARCHAR,
  -- Foreign key referencing meetstation(uri)
  foi_uri        VARCHAR,
  -- Foreign key referencing sensor(uri)
  sensor_uri     VARCHAR,
  -- Foreign key referencing procedure(uri)
  procedure_uri  VARCHAR,
  -- Foreign key referencing eigenschap(uri)
  eigenschap_uri VARCHAR,
  -- sosa:phenomenonTime → time:Interval → time:hasBeginning → time:inXSDDate
  begin_tijd     DATE,
  -- sosa:phenomenonTime → time:Interval → time:hasEnd → time:inXSDDate
  eind_tijd      DATE,
  -- sosa:resultTime
  result_tijd    TIMESTAMP,
  -- Foreign key referencing resultaat(uri)
  resultaat_uri  VARCHAR,
  PRIMARY KEY (uri)
);

COMMENT ON TABLE observatie IS 'http://www.w3.org/ns/sosa/Observation';
COMMENT ON COLUMN observatie.uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN observatie.foi_uri IS 'http://www.w3.org/ns/sosa/hasFeatureOfInterest';
COMMENT ON COLUMN observatie.sensor_uri IS 'http://www.w3.org/ns/sosa/madeBySensor';
COMMENT ON COLUMN observatie.procedure_uri IS 'http://www.w3.org/ns/sosa/usedProcedure';
COMMENT ON COLUMN observatie.eigenschap_uri IS 'http://www.w3.org/ns/sosa/observedProperty';
COMMENT ON COLUMN observatie.begin_tijd IS 'http://www.w3.org/2006/time#hasBeginning';
COMMENT ON COLUMN observatie.eind_tijd IS 'http://www.w3.org/2006/time#hasEnd';
COMMENT ON COLUMN observatie.result_tijd IS 'http://www.w3.org/ns/sosa/resultTime';
COMMENT ON COLUMN observatie.resultaat_uri IS 'http://www.w3.org/ns/sosa/hasResult';

----------------------------------------------------------------------

-- https://data.vlaanderen.be/ns/ssnsosa#ObservatieCollectie
-- Table type: JOIN
-- Original relation: heeft_lid_observatie
-- sosa:hasMember is M:N: één observatie kan lid zijn van meerdere collecties.
CREATE TABLE observatie_collectie_lid (
  -- Foreign key referencing observatie_collectie(uri)
  source_uri VARCHAR,
  -- Foreign key referencing observatie(uri)
  target_uri VARCHAR,
  PRIMARY KEY (source_uri, target_uri)
);

COMMENT ON TABLE observatie_collectie_lid IS 'http://www.w3.org/ns/sosa/ObservationCollection';
COMMENT ON COLUMN observatie_collectie_lid.source_uri IS 'http://example.org/vocab/uri';
COMMENT ON COLUMN observatie_collectie_lid.target_uri IS 'http://www.w3.org/ns/sosa/hasMember';

----------------------------------------------------------------------
-- Foreign key constraints
----------------------------------------------------------------------

ALTER TABLE meetstation ADD FOREIGN KEY (sample_van) REFERENCES studiegebied(uri);
ALTER TABLE sensor ADD FOREIGN KEY (host) REFERENCES meetstation(uri);
ALTER TABLE sensor ADD FOREIGN KEY (implementeert) REFERENCES procedure(uri);
ALTER TABLE sensor ADD FOREIGN KEY (observeert) REFERENCES eigenschap(uri);
ALTER TABLE observatie_collectie ADD FOREIGN KEY (foi_uri) REFERENCES meetstation(uri);
ALTER TABLE observatie_collectie ADD FOREIGN KEY (sensor_uri) REFERENCES sensor(uri);
ALTER TABLE observatie_collectie ADD FOREIGN KEY (procedure_uri) REFERENCES procedure(uri);
ALTER TABLE observatie_collectie ADD FOREIGN KEY (eigenschap_uri) REFERENCES eigenschap(uri);
ALTER TABLE resultaat ADD FOREIGN KEY (eenheid_uri) REFERENCES eenheid(uri);
ALTER TABLE observatie ADD FOREIGN KEY (foi_uri) REFERENCES meetstation(uri);
ALTER TABLE observatie ADD FOREIGN KEY (sensor_uri) REFERENCES sensor(uri);
ALTER TABLE observatie ADD FOREIGN KEY (procedure_uri) REFERENCES procedure(uri);
ALTER TABLE observatie ADD FOREIGN KEY (eigenschap_uri) REFERENCES eigenschap(uri);
ALTER TABLE observatie ADD FOREIGN KEY (resultaat_uri) REFERENCES resultaat(uri);
ALTER TABLE observatie_collectie_lid ADD FOREIGN KEY (source_uri) REFERENCES observatie_collectie(uri);
ALTER TABLE observatie_collectie_lid ADD FOREIGN KEY (target_uri) REFERENCES observatie(uri);
