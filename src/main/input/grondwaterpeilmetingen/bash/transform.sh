#!/bin/bash
xsltproc transformatie.xslt source.xml > /tmp/grondwaterpeilmetingen.rdf
riot --formatted=trig /tmp/grondwaterpeilmetingen.rdf > ../grondwaterpeilmetingen.trig
rm /tmp/grondwaterpeilmetingen.rdf
sparql --query query.sparql --data=../grondwaterpeilmetingen.trig --results=CSV > ../grondwaterpeilmetingen.csv
