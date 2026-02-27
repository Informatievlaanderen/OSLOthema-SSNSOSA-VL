#!/bin/bash

curl -O https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-EnergieManagementSystem/refs/heads/main/resources/datavoorbeelden/DatavoorbeeldStilleggingProductielijn.json
curl -O https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-EnergieManagementSystem/refs/heads/main/resources/datavoorbeelden/DatavoorbeeldSGerealiseerdeBesparing.json
curl -O https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-EnergieManagementSystem/refs/heads/main/resources/datavoorbeelden/DatavoorbeeldPreHeatingHvac.json
curl -O https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-EnergieManagementSystem/refs/heads/main/resources/datavoorbeelden/DatavoorbeeldIsolatieadvies.json
curl -O https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-EnergieManagementSystem/refs/heads/main/resources/datavoorbeelden/DatavoorbeeldHoofdaansluitingSubaansluiting.json

for i in *json ; do
  [[ -d ../${i/.json/}/source ]] || mkdir -p ../${i/.json/}/source
  mv $i ../${i/.json/}/source/${i/json/jsonld} ;
  riot --formatted=turtle prefixen.ttl ../${i/.json/}/source/${i/json/jsonld} > ../${i/.json/}/source/${i/json/ttl} ;
done

