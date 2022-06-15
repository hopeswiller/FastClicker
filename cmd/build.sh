#!/bin/bash

# Author : Hopeswiller
# Script follows here:

echo "Build Application into Executable"
cd ..
rm -rf build/ 
rm -rf dist/

pipenv run python setup.py clean

# pipenv run python setup.py build

pipenv run python setup.py bdist_msi 

rm -rf build/bdist.win*/

echo "Done..."