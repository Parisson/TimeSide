#/bin/sh

sed '/doctest/d' source/intro.rst | sed '/testcleanup/d' > ../README.rst
cat source/news.rst source/doc.rst source/install.rst source/ui.rst source/dev.rst source/related.rst source/copyright.rst >> ../README.rst

