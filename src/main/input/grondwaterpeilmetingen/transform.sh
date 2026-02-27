#!/bin/bash
xsltproc transformatie.xslt source.xml > grondwaterpeilmetingen.rdf
riot --formatted=turtle grondwaterpeilmetingen.rdf > grondwaterpeilmetingen.ttl
sparql --query query.sparql --data=grondwaterpeilmetingen.ttl --results=CSV > grondwaterpeilmetingen.csv
