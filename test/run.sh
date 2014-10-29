#!/bin/bash

export PYTHONPATH=../topydo/lib

if [ -n "$1" ]; then
  TESTS=$1
else
  TESTS="*Test.py"
fi

for TEST in $TESTS; do
  python -m unittest "${TEST%\.*}" # strip the .py extension
done
