#!/bin/bash

robot validate-profile --profile DL --input restrictie.ttl

robot reason --reasoner HermiT \
  --input restrictie.ttl \
  --axiom-generators "ClassAssertion" \
  --output afgeleid.ttl