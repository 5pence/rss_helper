 
 commands for celery runnings:
 
 celery -A rss_helper  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
 celery -A rss_helper worker -l info
