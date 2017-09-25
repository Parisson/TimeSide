#!/bin/sh

pip install -e git+git://github.com/michaeljones/sphinx-to-github.git#egg=sphinx-to-github

make install_deps
make html
make gh-pages
make readme
