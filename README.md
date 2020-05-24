 
 ### commands for celery:
 
 1. celery -A rss_helper  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
 
 2. celery -A rss_helper worker -l info

5 containers
    celery
    celery-beat
    redis
    postgres
    web (app)

git clone ...

# to clear docker ; docker-compose rm
docker-compose build
docker-compose up
docker-compose run web pipenv run /code/manage.py createsuperuser
docker-compose run web pipenv run /code/manage.py test



