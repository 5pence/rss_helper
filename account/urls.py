from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.welcome, name='welcome'),
    path('registration/', views.register, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('my_feeds/', views.my_feeds, name='my_feeds'),
    path('feed_item/<int:pk>/', views.feed_item_detail, name='feed_item'),
    path('feed_item/<int:pk>/add-comment', views.add_comment, name='add_comment'),
    path('delete-comment/<int:pk>', views.delete_comment, name='delete_comment'),
    path('toggle_bookmark/', views.toggle_favourite_feed_item, name='toggle_bookmark'),
]
