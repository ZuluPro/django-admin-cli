#!/bin/bash
# Package uploading to PyPI

version=$(python setup.py --version)
git rev-parse ${version} &> /dev/null
if [[ "$?" -eq 0 ]] ; then
    echo "Version '${version}' already exists."
    exit 1
fi
git tag -a ${version} -m "Version ${version}"
git push origin ${version}
python setup.py sdist
twine upload dist/*
