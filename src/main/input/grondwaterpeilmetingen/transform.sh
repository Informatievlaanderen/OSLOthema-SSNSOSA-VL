#!/bin/bash
xsltproc transformatie.xslt source.xml > grondwaterpeilmetingen.rdf
#riot --output=turtle /home/gehau/git/OSLOthema-SSNSOSA-VL/src/main/input/grondwaterpeilmetingen/grondwaterpeilmetingen.rdf | sed -e 's/_:/ex:/g' > /tmp/grondwaterpeilmetingen.ttl
#riot --formatted=turtle /tmp/grondwaterpeilmetingen.ttl > grondwaterpeilmetingen.ttl
riot --formatted=turtle grondwaterpeilmetingen.rdf > grondwaterpeilmetingen.ttl
sparql --query query.sparql --data=grondwaterpeilmetingen.ttl --results=CSV > grondwaterpeilmetingen.csv
