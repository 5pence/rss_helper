from django.contrib import admin
from account.models import Feed, FeedItem


class FeedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'last_checked_at', 'fail_count']


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'feed']
    list_filter = ['feed']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
