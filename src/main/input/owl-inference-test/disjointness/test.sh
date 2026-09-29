#!/bin/bash

robot explain --reasoner HermiT \
  --input test.ttl \
  --mode inconsistency \
  --explanation uitleg.md

robot reason --reasoner HermiT \
  --input test.ttl \
  --axiom-generators "ClassAssertion" \
  --output afgeleid.ttl