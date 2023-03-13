from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('main', views.main, name='main'),
    path('client', views.clients, name='client'),
    path('client/<int:client_id>', views.client_info, name='client_info'),
]