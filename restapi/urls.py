from django.contrib import admin
from django.urls import path,include
from restapi import views


from django.urls import path, include
from . import views

urlpatterns= [
    #path('Event/',EventsView.as_view(), name = 'EventsView'),
    #path('/',, name = ,'EventsView'),
    #path('get/details',views.showDetails, name = 'showDetails'),
    #path('get/registrations',views.showRegistrationsAndParticipations, name = 'showRegistrationsAndParticipations'),
    #path('get/event', views.showEvent, name = 'showEvent'),
    path('events/newgame',views.newGame, name = 'newGame'),
    path('events/addplayer',views.appendPlayers, name = 'appendPlayer'),
    path('events/endgame',views.endGame, name = 'endGame'),
    path('register/fetch',views.getUserEvent, name = 'getUserEvent'),
    path('register/push',views.modifyRegistrationsAndParticipations, name = 'modifyRegistrationsAndParticipations'),
]