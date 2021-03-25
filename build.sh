#!/bin/bash

python setup.py sdist bdist_wheel

twine check dist/*
twine upload dist/* --verbose


# or run
rm confo.egg-info/ dist/ build -rf && python setup.py sdist bdist_wheel && twine check dist/*
#then
twine upload dist/* --verbose

