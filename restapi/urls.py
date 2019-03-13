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
    
    #this is to add a new game
    path('events/newgame',views.newGame, name = 'newGame'),
    #this is to append players to an existing team
    path('events/addplayer',views.appendPlayers, name = 'appendPlayer'),
    #this is to update status of game to played and update the points
    path('events/endgame',views.endGame, name = 'endGame'),
    #this is to fetch both the played and not played games which are registered by user
    path('register/fetch',views.getUserEvent, name = 'getUserEvent'),
    #this is to modify the event details with paid and payment mode details
    path('register/push',views.modifyRegistrationsAndParticipations, name = 'modifyRegistrationsAndParticipations'),
]
