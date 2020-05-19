from django.contrib import admin
from account.models import Feed, FeedItem


class FeedAdmin(admin.ModelAdmin):
    pass


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'feed']
    list_filter = ['feed']


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
