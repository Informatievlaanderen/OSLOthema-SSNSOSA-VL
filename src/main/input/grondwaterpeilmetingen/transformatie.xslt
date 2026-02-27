<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:sosa="http://www.w3.org/ns/sosa/"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
                xmlns:gml="http://www.opengis.net/gml/3.2"
                xmlns:ex="http://example.org/"
                xmlns:geo="http://www.opengis.net/ont/geosparql#"
                xmlns:qudt="http://qudt.org/vocab/unit#"
                xmlns:ns4="http://kern.schemas.dov.vlaanderen.be"
                xmlns:put="https://www.dov.vlaanderen.be/data/put/"
                xmlns:filter="https://www.dov.vlaanderen.be/data/filter/"
                xmlns:dct="http://purl.org/dc/terms/"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                exclude-result-prefixes="xsl">

    <xsl:output method="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:output indent="yes"/>

    <xsl:template match="/">
        <rdf:RDF>
            <xsl:apply-templates select="/ns4:dov-schema/grondwaterlocatie"/>
            <xsl:apply-templates select="/ns4:dov-schema/filter"/>
            <xsl:apply-templates select="//peilmeting"/>
        </rdf:RDF>
    </xsl:template>

    <xsl:template match="filter">
        <rdf:Description>
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="/ns4:dov-schema/filter/dataidentifier/uri"/>
            </xsl:attribute>
            <xsl:attribute name="rdf:type">
                <xsl:value-of select="'http://www.w3.org/ns/sosa/System'"/>
            </xsl:attribute>
            <sosa:isHostedBy>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="/ns4:dov-schema/grondwaterlocatie/dataidentifier/uri"/>
                    </xsl:attribute>
                </rdf:Description>
            </sosa:isHostedBy>
            <dct:author>
                <xsl:value-of select="concat(opmerking/auteur/voornaam, ' ', opmerking/auteur/naam)"/>
            </dct:author>
            <rdfs:comment>
                <xsl:value-of select="opmerking/tekst"/>
            </rdfs:comment>

        </rdf:Description>
        <xsl:apply-templates select="opbouw/onderdeel"/>
    </xsl:template>


    <xsl:template match="onderdeel">
        <rdf:Description>
            <xsl:attribute name="rdf:type">
                <xsl:value-of select="'http://www.w3.org/ns/sosa/System'"/>
            </xsl:attribute>
            <sosa:isHostedBy>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="/ns4:dov-schema/grondwaterlocatie/dataidentifier/uri"/>
                    </xsl:attribute>
                </rdf:Description>
            </sosa:isHostedBy>
            <sosa:isSubSystemOf>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="/ns4:dov-schema/filter/dataidentifier/uri"/>
                    </xsl:attribute>
                </rdf:Description>
            </sosa:isSubSystemOf>
            <ex:van rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                <xsl:value-of select="van"/>
            </ex:van>
            <ex:tot rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                <xsl:value-of select="tot"/>
            </ex:tot>
            <ex:filterelement>
                <xsl:value-of select="filterelement"/>
            </ex:filterelement>
            <ex:materiaal>
                <xsl:value-of select="materiaal"/>
            </ex:materiaal>
            <ex:binnendiameter rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                <xsl:value-of select="binnendiameter"/>
            </ex:binnendiameter>
        </rdf:Description>

    </xsl:template>

    <xsl:template match="peilmeting">
        <rdf:Description>
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="concat('http://example.org/peilmeting_', datum)"/>
            </xsl:attribute>
            <rdf:type rdf:resource="http://www.w3.org/ns/sosa/ObservationCollection"/>
            <sosa:hasMember>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="concat('http://example.org/peilmeting_', datum, 'diepte_tov_referentiepunt')"/>
                    </xsl:attribute>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/Observation"/>
                    <sosa:hasResult>
                        <rdf:Description>
                            <rdf:type rdf:resource="http://www.w3.org/ns/sosa/Result"/>
                            <rdf:value  rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                                <xsl:value-of select="diepte_tov_referentiepunt"/>
                            </rdf:value>
                            <qudt:unit  rdf:resource="http://qudt.org/vocab/unit#Meter"/>
                        </rdf:Description>
                    </sosa:hasResult>
                    <sosa:observedProperty rdf:resource="http://example.org/diepte_tov_referentiepunt"/>
                    <sosa:usedProcedure>
                        <xsl:attribute name="rdf:resource">
                            <xsl:value-of select="translate(concat('http://example.org/', methode, '_methode'), ' ', '')"/>
                        </xsl:attribute>
                    </sosa:usedProcedure>
                </rdf:Description>
            </sosa:hasMember>
            <sosa:hasMember>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="concat('http://example.org/peilmeting_', datum, 'peil_mtaw')"/>
                    </xsl:attribute>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/sosa:Observation"/>
                    <sosa:hasResult>
                        <rdf:Description>
                            <rdf:type rdf:resource="http://www.w3.org/ns/sosa/Result"/>
                            <rdf:value  rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                                <xsl:value-of select="peil_mtaw"/>
                            </rdf:value>
                            <qudt:unit  rdf:resource="http://qudt.org/vocab/unit#Meter"/>
                        </rdf:Description>
                    </sosa:hasResult>
                    <sosa:observedProperty rdf:resource="http://example.org/peil_mtaw"/>
                    <sosa:usedProcedure>
                        <xsl:attribute name="rdf:resource">
                            <xsl:value-of select="translate(concat('http://example.org/', methode, '_methode'), ' ', '')"/>
                        </xsl:attribute>
                    </sosa:usedProcedure>
                </rdf:Description>
            </sosa:hasMember>
            <sosa:hasMember>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="concat('http://example.org/peilmeting_', datum, 'filtertoestand')"/>
                    </xsl:attribute>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/sosa:Observation"/>
                    <sosa:hasSimpleResult rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
                        <xsl:value-of select="filtertoestand"/>
                    </sosa:hasSimpleResult>
                    <sosa:observedProperty rdf:resource="http://example.org/filtertoestand"/>
                    <sosa:usedProcedure rdf:resource="http://example.org/visueel_methode"/>
                </rdf:Description>
            </sosa:hasMember>
            <sosa:hasMember>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="concat('http://example.org/peilmeting_', datum, 'filterstatus')"/>
                    </xsl:attribute>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/sosa:Observation"/>
                    <sosa:hasSimpleResult rdf:datatype="http://www.w3.org/2001/XMLSchema#string">
                        <xsl:value-of select="filterstatus"/>
                    </sosa:hasSimpleResult>
                    <sosa:observedProperty rdf:resource="http://example.org/filterstatus"/>
                    <sosa:usedProcedure rdf:resource="http://example.org/visuele_controle"/>
                </rdf:Description>
            </sosa:hasMember>
            <sosa:hasMember>
                <rdf:Description>
                    <xsl:attribute name="rdf:about">
                        <xsl:value-of select="concat('http://example.org/peilmeting_', datum, 'zoet')"/>
                    </xsl:attribute>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/sosa:Observation"/>
                    <sosa:hasSimpleResult rdf:datatype="http://www.w3.org/2001/XMLSchema#string">
                        <xsl:value-of select="zoet"/>
                    </sosa:hasSimpleResult>
                    <sosa:observedProperty rdf:resource="http://example.org/zoet"/>
                    <sosa:usedProcedure rdf:resource="http://example.org/smaaktest"/>
                </rdf:Description>
            </sosa:hasMember>
            <sosa:madeBySensor >
                <rdf:Description>
                    <rdf:type rdf:resource="http://www.w3.org/ns/sosa/Sensor"/>
                    <rdfs:label>
                        <xsl:value-of select="opmeter/naam"/>
                    </rdfs:label>
                </rdf:Description>
            </sosa:madeBySensor>
            <sosa:hasFeatureOfInterest >
                <xsl:attribute name="rdf:resource">
                    <xsl:value-of select="/ns4:dov-schema/grondwaterlocatie/dataidentifier/uri"/>
                </xsl:attribute>
            </sosa:hasFeatureOfInterest>
            <sosa:resultTime rdf:datatype="http://www.w3.org/2001/XMLSchema#date">
                <xsl:value-of select="datum"/>
            </sosa:resultTime>
        </rdf:Description>

    </xsl:template>
    <xsl:template match="grondwaterlocatie">
        <rdf:Description>
            <xsl:attribute name="rdf:about">
                <xsl:value-of select="/ns4:dov-schema/grondwaterlocatie/dataidentifier/uri"/>
            </xsl:attribute>
            <xsl:attribute name="rdf:type">
                <xsl:value-of select="'http://www.w3.org/ns/sosa/Platform'"/>
            </xsl:attribute>
            <geo:hasGeometry>
                <rdf:Description>
                    <rdf:type rdf:resource="http://www.opengis.net/ont/geosparql#Geometry"/>
                    <geo:asGML rdf:datatype="http://www.opengis.net/ont/geosparql#gmlLiteral">
                        <xsl:text disable-output-escaping="no">&lt;gml:Point srsName="</xsl:text>
                        <xsl:value-of select="ligging/gml:Point/@srsName"/>
                        <xsl:text disable-output-escaping="no">" srsDimension="</xsl:text>
                        <xsl:value-of select="ligging/gml:Point/@srsDimension"/>
                        <xsl:text disable-output-escaping="no">"&gt; &lt;gml:pos&gt;</xsl:text>
                        <xsl:value-of select="ligging/gml:Point/gml:pos"/>
                        <xsl:text disable-output-escaping="no">&lt;/gml:pos&gt; &lt;/gml:Point&gt;</xsl:text>
                    </geo:asGML>
                </rdf:Description>
            </geo:hasGeometry>

        </rdf:Description>
    </xsl:template>

</xsl:stylesheet>