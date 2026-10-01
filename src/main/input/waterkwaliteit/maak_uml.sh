#!/bin/bash
 python3 scripts/ontologie_naar_uml.py                              # → waterkwaliteit_uml.mmd
mmdc -i waterkwaliteit_uml.mmd -o waterkwaliteit_uml.svg -b white  # → waterkwaliteit_uml.