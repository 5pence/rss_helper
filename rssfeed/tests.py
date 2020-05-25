from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rssfeed.models import Feed, FeedItem
from feed.tasks import import_feed_task
from django.utils import timezone


class FeedTest(TestCase):
    def setUp(self):
        """ Set up our test user """
        password = 'reallySecure#123'
        self.user = User.objects.create(
            username='test@test.com',
            password=password,
            is_active=True
        )
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.username, password=password)

    def test_add_feed_success(self):
        """ Add a feed and ensure the added feed message is displayed on page """
        url = reverse('add_feed')
        # Get the count of feeds
        before_count = self.user.feed_set.all().count()
        response = self.client.post(
            url,
            data={
                'title': 'random feed',
                'url': 'http://www.nu.nl/rss/Algemeen'
            })
        # Assert status code is OK
        self.assertEqual(response.status_code, 200)
        # Assert message is displayed on page
        self.assertContains(response, 'Your feed was added, '
                                      'it may take up to a minute for you '
                                      'to see some feed items')
        # Get the current count of feeds
        after_count = self.user.feed_set.all().count()
        # Assert we have an additional one
        self.assertEqual(after_count - before_count, 1)

    def test_add_feed_fail_no_auth(self):
        """ Check an unauthorised user cannot add a feed """
        # Create a client
        c = Client()
        # Go to add feed page
        url = reverse('add_feed')
        # Count current number of feeds
        before_count = self.user.feed_set.all().count()
        # Attempt to add a feed
        response = c.post(
            url,
            data={
                'title': 'random feed',
                'url': 'https://google.com/xml'
            })
        # Check we re redirected as we are unauthorised
        self.assertEqual(response.status_code, 302)
        # Check no feeds were added to the database
        self.assertEqual(before_count, self.user.feed_set.all().count())

    def test_add_feed_fail_bad_url(self):
        """ Test adding a feed with a bad url string that isn't a rss feed """
        url = reverse('add_feed')
        # Count all feeds
        before_count = self.user.feed_set.all().count()
        # Post a feed with a bad url
        response = self.client.post(
            url,
            data={
                'title': 'random feed',
                'url': 'https://google.com/xml'
            })
        self.assertEqual(response.status_code, 200)
        # Check the two error messages are returned on page
        self.assertContains(response, 'Invalid RSS Feed')
        # Check no feed was added

        self.assertEqual(before_count, self.user.feed_set.all().count())

    def test_add_feed_fail_duplicate_title(self):
        """ Test adding a feed with a duplicate title string """
        for i in range (0, 2):
            url = reverse('add_feed')
            # Count all feeds
            before_count = self.user.feed_set.all().count()
            # Post a feed with a bad url
            response = self.client.post(
                url,
                data={
                    'title': 'random feed',
                    'url': 'http://www.nu.nl/rss/Algemeen'
                })
            self.assertEqual(response.status_code, 200)
        # Check the two error messages are returned on page
        self.assertContains(response, 'You already have that title in your feed, please choose another.')
        # Check no feed was added
        self.assertEqual(before_count, self.user.feed_set.all().count())

    def test_update_feed(self):
        """ Test to update feed details """
        feed = Feed.objects.create(
            user=self.user,
            title='random feed',
            url='http://www.nu.nl/rss/Algemeen'
        )
        url = reverse('update_feed', kwargs={'pk': feed.id})
        before_count = self.user.feed_set.all().count()
        response = self.client.post(
            url,
            data={
                'title': 'another random feed',
                'url': 'http://www.nu.nl/rss/Algemeen'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "successfully updated your feed")
        self.assertContains(response, "another random feed")
        after_count = self.user.feed_set.all().count()
        # ensure no duplicates were made
        self.assertEqual(before_count, after_count)

    # def test_add_bookmark(self):
    #     feed = Feed.objects.create(
    #         user=self.user,
    #         title='random feed',
    #         url='http://www.nu.nl/rss/Algemeen'
    #     )

    def test_unread_count(self):
        """ Add a feed, a feed item and check the is_read counter is 1 then No unread items"""
        # create a feed
        feed = Feed.objects.create(
            user=self.user,
            title='random feed',
            url='http://www.nu.nl/rss/Algemeen'
        )
        # add a feed item to feed
        feeditem = FeedItem.objects.create(
            feed=feed,
            title='great feed item',
            text='some text about great feed item',
            url='https://google.com'
        )
        # goto my_feeds page
        url = reverse('my_feeds')
        response = self.client.get(url)
        # make sure Unread items:1 is on page
        self.assertContains(response, 'Unread items')
        self.assertContains(response, '<mark>1</mark>')
        # now visit that feed item
        url = reverse('feed_item', kwargs={'pk': feeditem.id})
        response = self.client.get(url)
        # ensure the text of the feed item is present
        self.assertContains(response, 'great feed item')
        # go back to my_feeds
        url = reverse('my_feeds')
        # Ensure that 'No unread items' is on page
        response = self.client.get(url)
        self.assertContains(response, 'No unread items')

    def test_remove_feed(self):
        feed = Feed.objects.create(
            user=self.user,
            title='random feed',
            url='http://www.nu.nl/rss/Algemeen'
        )
        url = reverse('my_feeds')
        response = self.client.get(url)
        self.assertContains(response, 'random feed')
        url = reverse('remove_feed', kwargs={'pk': feed.id})

    # def test_add_comment(self):
    #     feed = Feed.objects.create(
    #         user=self.user,
    #         title='random feed',
    #         url='http://www.nu.nl/rss/Algemeen'
    #     )

    def test_remove_comment(self):
        feed = Feed.objects.create(
            user=self.user,
            title='random feed',
            url='http://www.nu.nl/rss/Algemeen'
        )

    def test_feed_import_fail_backoff(self):
        """ Test exponential backoff algorithm by using a bad feed url
        and ensures a restart button is present after 10 failed tests on the My Feeds page
        """
        feed = Feed.objects.create(
            title='test',
            url='https://google.com/xml',
            user=self.user
        )
        # Loop the fail 11 times
        for i in range(0, 11):
            # get the feed
            import_feed_task(feed.id)
            # refresh what's being held in the database
            feed.refresh_from_db()
            # assert the fail count increased by 1
            self.assertEqual(feed.fail_count, i + 1)
            # calculate the next feed time 2 exponential fail count
            next_run_datetime = timezone.now() + timedelta(minutes=2 ** feed.fail_count)
            """ Due to microseconds being in the datetime object and local timezone.now() 
            minutely different to the database timezone.now() we assert our calculated time
            is almost equal within 1 second to the actual time recorded in database 
            """
            self.assertAlmostEqual(
                feed.last_checked_at,
                next_run_datetime,
                delta=timezone.timedelta(seconds=1)
            )
        # Now get the content of my feeds page
        response = self.client.get('/rssfeed/my_feeds/')
        # As the feed has failed over 10 times assert failed message is on page
        self.assertContains(response, 'Sorry, this feed has failed many times')
        # And that the button labelled 'Restart Feed' is present
        self.assertContains(response, 'Restart Feed')
