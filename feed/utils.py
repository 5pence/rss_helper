import feedparser
from account.models import FeedItem
from django.db.utils import IntegrityError


def fetch_rss(url):
    return feedparser.parse(url)


def import_items(feed):
    xml = fetch_rss(feed.url)
    for entry in xml.entries:
        try:
            item = FeedItem.objects.create(
                feed=feed,
                title=entry.title,
                text=entry.description,
                url=entry.link
            )
        except IntegrityError:
            pass
