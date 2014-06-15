#!/bin/bash

PYTHONPATH=..

if [ -n "$1" ]; then
  TESTS=$1
else
  TESTS="FilterTest SorterTest TodoBaseTest TodoFileTest TodoTest TodoListTest"
fi

for TEST in $TESTS; do
  python -m unittest "$TEST"
done
