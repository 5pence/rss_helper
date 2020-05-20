from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.welcome, name='welcome'),
    path('registration/', views.register, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

]
