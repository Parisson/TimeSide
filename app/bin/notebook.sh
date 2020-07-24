# How-to use:
# docker-compose -f docker-compose.yml -f env/notebook.yml run --service-ports notebook sh bin/notebook.sh
cd /srv/lib/timeside/docs/ipynb
jupyter notebook --no-browser --ip=0.0.0.0 --allow-root
