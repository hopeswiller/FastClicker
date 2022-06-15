#!/bin/bash

# Author : Hopeswiller
# Script follows here:

echo "Compiling Requirements File "
cd ..

pipenv requirements > requirements.txt
# pipenv requirements --dev-only > requirements-dev.txt


echo "Done... "