cd /srv/src/timeside/
conda env create --name app --force --file environment.yml
#python setup.py test
conda env export --name app --file environment-pinned.yml
