#!/bin/bash
xsltproc transformatie.xslt source.xml > grondwaterpeilmetingen.rdf
riot --formatted=trig grondwaterpeilmetingen.rdf > grondwaterpeilmetingen.trig
sparql --query query.sparql --data=grondwaterpeilmetingen.trig --results=CSV > grondwaterpeilmetingen.csv
