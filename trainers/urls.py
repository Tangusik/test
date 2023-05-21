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
    path('client/add', views.client_add, name='client_add'),
    path('client/add/action', views.client_add_action, name='client_add_action'),
    path('teams', views.teams, name='teams'),
    path('team/<int:team_id>', views.team_info, name='team_info'),
    path('teams/add', views.team_add, name='team_add'),
    path('teams/add/action', views.team_add_action, name='team_add_action'),
    path('trainers', views.trainers, name='trainers'),
    path('trainers/add', views.trainers_add, name='trainers_add'),
    path('trainers/add_action', views.trainers_add_action, name='trainers_add_action'),
    path('trainers/<int:trainer_id>', views.trainer_info, name='trainer_info'),
    path('activities', views.activity, name='activity'),
    path('activities/<int:activity_id>', views.activity_info, name='activity_info'),
    path('activities/<int:activity_id>/change', views.activity_change, name='act_change'),

]