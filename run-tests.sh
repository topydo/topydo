#!/bin/bash

if [ "$1" = "python2" ] || [ "$1" = "python3" ]; then
  PYTHON=$1
else
  # run whatever is active
  PYTHON=python
fi

# Run normal tests
if ! $PYTHON setup.py test; then
  exit 1
fi

# pylint is not supported on 3.2, so skip the test there
if $PYTHON --version 2>&1 | grep 'Python 3\.2' > /dev/null; then
  exit 0
fi

if ! $PYTHON -m pylint --errors-only topydo test; then
  exit 1
fi

exit 0

