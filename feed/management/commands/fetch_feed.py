from django.core.management.base import BaseCommand, CommandError
from feed.utils import import_items
from account.models import Feed


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str)
        parser.add_argument('--id', type=int)

    def handle(self, *args, **options):
        feed = Feed.objects.get(pk=options['id'])
        print(feed.url)
        print(import_items(feed))