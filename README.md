 
 ### commands for celery:
 
 1. celery -A rss_helper  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
 
 2. celery -A rss_helper worker -l info
