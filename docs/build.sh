#!/bin/sh

pip install -e git+git://github.com/michaeljones/sphinx-to-github.git#egg=sphinx-to-github

make install_deps
make gh-pages
make readme
