import logging

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from celery import shared_task
from rssfeed.models import Feed
from feed.utils import import_items, ImportFailed

logger = logging.getLogger(__name__)


@shared_task
def import_feed_task(feed_id: int):
    logger.info('fetching id %d' % feed_id)
    feed = Feed.objects.get(pk=feed_id)
    try:
        import_items(feed)
        feed.last_checked_at = timezone.now()
        feed.fail_count = 0
    except ImportFailed:
        """ If for any reason the fetching of the remote xml fails we will increase a fail counter
        the fail counter is also a threshold, after X number of fails don't bother
        we set last_checked_at to the future, our import_feeds checks only for feeds that
        were last checked in the past. """
        feed.fail_count += 1
        feed.last_checked_at = timezone.now() + timedelta(minutes=(2 ** feed.fail_count))
    feed.save()


@shared_task
def import_feeds():
    """ Search for feeds that are in need of updating
    ignore any feeds that have surpassed a certain configurable threshold
    see settings to update FAIL_COUNT_THRESHOLD to a suitable value """
    fail_count_threshold = settings.FAIL_COUNT_THRESHOLD
    feeds = Feed.objects.filter(last_checked_at__lte=timezone.now(), fail_count__lte=fail_count_threshold)
    for feed in feeds:
        import_feed_task.delay(feed.id)
