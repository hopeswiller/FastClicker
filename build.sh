#!/bin/bash

# Author : Hopeswiller
# Script follows here:

echo "Build Application into Executable"

pipenv run python setup.py clean

pipenv run python setup.py build
