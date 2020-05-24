import feedparser
from rssfeed.models import FeedItem
from django.db.utils import IntegrityError


class ImportFailed(Exception):
    pass


def fetch_rss(url):
    return feedparser.parse(url)


def import_items(feed):
    try:
        xml = fetch_rss(feed.url)
        if 'bozo' in xml and xml['bozo'] == 1:
            raise ImportFailed
    except:
        raise ImportFailed
    for entry in xml.entries:
        try:
            item = FeedItem.objects.create(
                feed=feed,
                title=entry.title,
                text=entry.description,
                url=entry.link
            )
        except IntegrityError:
            # This exception is raised when we hit duplicates.  Duplicates are ignored as
            # it's cheaper to try to insert them, rather than to lookup and check if it exists
            # then insert if it does not.
            pass
