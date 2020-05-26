from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('add_feed', views.add_feed, name='add_feed'),
    path('update_feed/<int:pk>', views.update_feed, name='update_feed'),
    path('my_feeds/', views.my_feeds, name='my_feeds'),
    path('remove_feed/<int:pk>', views.remove_feed, name='remove_feed'),
    path('my_favourite_feeds/', views.my_favourite_feeds, name='my_favourite_feeds'),
    path('feed_item/<int:pk>/', views.feed_item_detail, name='feed_item'),
    path('feed_item/<int:pk>/add-comment', views.add_comment, name='add_comment'),
    path('delete-comment/<int:pk>', views.delete_comment, name='delete_comment'),
    path('toggle_bookmark/<int:pk>', views.toggle_favourite_feed_item, name='toggle_bookmark'),
    path('reset_fail_count/<int:pk>', views.reset_fail_count, name='reset_fail_count'),
]
