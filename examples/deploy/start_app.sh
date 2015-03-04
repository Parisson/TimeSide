python /opt/TimeSide/examples/sandbox/manage.py syncdb --noinput
python /opt/TimeSide/examples/sandbox/manage.py migrate --noinput
python /opt/TimeSide/examples/sandbox/manage.py collectstatic --noinput

uwsgi --socket :8000 --wsgi-file /opt/TimeSide/examples/sandbox/wsgi.py  --chdir /opt/TimeSide/examples/sandbox/ --master --processes 4 --threads 2