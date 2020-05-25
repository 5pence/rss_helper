from django.core.management.base import BaseCommand
from feed.tasks import import_feed_task
from rssfeed.models import Feed


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str)
        parser.add_argument('--id', type=int)

    def handle(self, *args, **options):
        feed = Feed.objects.get(pk=options['id'])
        import_feed_task.delay(feed.id)
