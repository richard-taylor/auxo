#!/bin/bash

TOP=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

export PYTHONPATH=$TOP

# run the python unit tests

cd $TOP/auxo/test
python3 -m unittest
