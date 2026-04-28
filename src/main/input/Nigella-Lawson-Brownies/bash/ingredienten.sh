#!/bin/bash


cat <<EOF > /tmp/query.sparql
PREFIX p-plan: <http://purl.org/net/p-plan#>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX unit: <http://qudt.org/vocab/unit/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?ingredient ?value ?unit
WHERE {

  ?ingredient a p-plan:Variable ;
              qudt:quantityValue ?q .

  ?q qudt:numericValue ?value ;
     qudt:hasUnit ?unit .

}
ORDER BY ?ingredient
EOF
sparql --query /tmp/query.sparql --data=../Nigella-Lawson-Brownies.ttl --results=CSV > ingredienten.csv
