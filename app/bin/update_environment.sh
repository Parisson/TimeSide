# This script update the environment with up-to-date dependencies
# from the specification provides by conda-environment.yml
# and pinned the packages version in environment-pinned.yml

# Please test the environment before committing changes to environment-pinned.yml
# `python setup.py test`

cd /srv/lib/timeside/
conda env create --name app --force --file conda-environment.yml
#python setup.py test
conda env export --name app --file environment-pinned.yml
