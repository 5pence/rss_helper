pipenv run python /code/manage.py migrate
pipenv run /code/manage.py loaddata init.json
pipenv run /code/manage.py collectstatic --noinput
#pipenv run python /code/manage.py runserver 0.0.0.0:8001
pipenv run gunicorn rss_helper.wsgi -b 0.0.0.0:8001