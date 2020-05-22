from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Feed
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
                'description': 'Best feed ever',
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
                'description': 'Best feed ever',
                'url': 'https://google.com/xml'
            })
        # Check we re redirected as we are unauthorised
        self.assertEqual(response.status_code, 302)
        # Check no feeds were added to the database
        self.assertEqual(before_count, self.user.feed_set.all().count())

    def test_add_feed_fail_bad_body(self):
        """ Test adding a feed with a bad url string that isn't a rss feed """
        url = reverse('add_feed')
        # Count all feeds
        before_count = self.user.feed_set.all().count()
        # Post a feed with a bad url
        response = self.client.post(
            url,
            data={
                'name': 'random feed',
                'description': 'Best feed ever',
                'url': 'https://google.com/xml'
            })
        self.assertEqual(response.status_code, 200)
        # Check the two error messages are returned on page
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'Invalid RSS Feed')
        # Check no feed was added
        self.assertEqual(before_count, self.user.feed_set.all().count())

    def test_feed_import_fail_backoff(self):
        """ Test exponential backoff algorithm by using a bad feed url
        and ensures a restart button is present after 10 failed tests on the My Feeds page
        """
        feed = Feed.objects.create(
            title='test',
            description='',
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
        response = self.client.get('/account/my_feeds/')
        # As the feed has failed over 10 times assert failed message is on page
        self.assertContains(response, 'Sorry, this feed has failed many times')
        # And that the button labelled 'Restart Feed' is present
        self.assertContains(response, 'Restart Feed')
