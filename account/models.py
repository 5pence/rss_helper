from django.db import models
from django.contrib.auth import get_user_model


class TitleMixin(object):
    def __str__(self):
        return self.title


class Feed(TitleMixin, models.Model):
    """ Model for the RSS Feed """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def unread(self):
        """ Helper function to return sum of unread feed items"""
        return self.feeditem_set.filter(is_read=False).count()


class FeedItem(TitleMixin, models.Model):
    """ Model that relates to a feed item of a feed """
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    # set is_read and is_bookmarked as  additional indexes for faster look up
    is_read = models.BooleanField(default=False, db_index=True)
    is_bookmarked = models.BooleanField(default=False, db_index=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        """ Ensures duplicate feed items are not saved"""
        unique_together = ['feed', 'title']