#!/usr/bin/env bash

rm -r dist
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u ikamensh