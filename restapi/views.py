from django.shortcuts import render

# Create your views here.

from rest_framework import generics,viewsets
from acusite.models import Profile,EventDetails,Event,Team
from .serializers import ProfileSerializer,EventSerializer,EventDetailsSerializer,TeamSerializer,PaymentDeskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.db.models import F
import json

from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

#-----------------------------------------------------------------------------------

#PAYMENT DESK



@csrf_protect
def cost(request):
    qr_code = request.POST.get("qr_code")
    pro = Profile.objects.get(qr_code=qr_code)
    no_of_events_for_pro = EventDetails.objects.filter(qr_code=pro).__len__()
    pro.cost = 200 if no_of_events_for_pro == 12 else (
        ((no_of_events_for_pro // 3) * 100) + ((no_of_events_for_pro % 3) * 40)
    )
    pro.save()

    return pro.cost




# URL register/fetch
@csrf_protect
def getUserEvent(request):

    message='Error'
    if request.method == 'POST':
        try:
            qr_code=request.POST.get("qr_code")

            pro = Profile.objects.get(qr_code=qr_code)

        except ObjectDoesNotExist:
            return HttpResponse("QR Code is not valid",content_type="text/plain")

        #sending all registered events both paid and not paid , we disable register for the events paid in app
        queryset=EventDetails.objects.filter(qr_code=qr_code)

        no_of_events_for_pro = EventDetails.objects.filter(qr_code=qr_code).__len__()
        pro.cost = 200 if no_of_events_for_pro == 12 else (
            ((no_of_events_for_pro // 3) * 100) + ((no_of_events_for_pro % 3) * 40)
        )
        pro.save()
        json_data = serializers.serialize('json', [queryset,pro])
        return HttpResponse(json_data, content_type="application/json")


    else:
        message="wrong method called"
        return HttpResponse(message,content_type="text/plain")






# URL register/push
@csrf_protect
def modifyRegistrationsAndParticipations(request):
    message="Error"
    if request.method=='POST':
        qr_code = request.POST.get("qr_code")
        profile = Profile.objects.get(qr_code=qr_code)

        #queryset =EventDetails.objects.filter(qr_code=profile)

        #if the jason format has [{qid:qid},{events:[(event ids,paymentmode)]}]

        eventlist=request.POST.get('events')

        for event_id in eventlist:

            obj=EventDetails.objects.get(qr_code=qr_code,event_id=event_id)
            obj.paid= True
            obj.payment_mode=payment_mode
            obj.save()

        message="Successfully Updated"

        return HttpResponse(message, content_type="text/plain")
    else:
        message = 'Invalid Request'

    return HttpResponse(message, content_type="text/plain")


#---------------------------------------------------------------------------------------------------------
# EVENT ORGANISER

#For checking the user is playing for first time or is he a valid player

@csrf_protect
def validateGame(event_id,qr_code):

    try:
        eventdetails = Profile.objects.filter(qr_code=qr_code,event_id=event_id)
    except ObjectDoesNotExist:
            return HttpResponse("Didn't registered for this Game",content_type="text/plain")

    queryset = EventDetails.objects.get(qr_code=details,event_id=eid)

    if (queryset.paid==True):

        return True

    else:
        return False


#For starting a new game with single qr_code
#URL events/newgame

@csrf_protect
def newGame(request):

    Message='Error'

    if request.method=='POST':
        event_id=request.POST.get('event_id')
        qr_code=request.POST.get('qr_code')

        if isEligible(event_id,qr_code):

            team_id=generateTeamId(event_id)

            eventdetail=EventDetails.objects.filter(qr_code=qr_code,event_id=event_id)
            eventdetail.status_choice="RUNNING"
            eventdetail.team_id =team_id
            eventdetail.save()

            team=Team(team_id=team_id,event_id=event_id,team_size=1)
            team.save()

            profile=Profile.objects.get(qr_code=qr_code)

            json_data=serializers.serialize('json',[eventdetail,profile])
            return HttpResponse(json_data,content_type="application/json")

        else :

            message= 'User is not Allowed to Play'
    else:
        message='Not a Valid Request'

    return HttpResponse(message,content_type="text/plain")










#Generates unique GID which doesn't occur in the data base
@csrf_protect
def generateGID(event_id):

    event=EventDetails.objects.get(event_id=event_id)
    event.event_count=event.event_count+1
    event.save()
    return "%s%s%s" %(event_id,event_id,event.event_count)


#Takes Existing Gid and adds Players
# URL @ events/addplayer
@csrf_protect
def appendPlayers(request):

    Message="Error in requesting method"

    if request.method=='POST':
        qr_code=request.objects.get('qr_code')
        team_id=request.objects.get('team_id')

        try:
            queryset=Team.objects.get(team_id=team_id)

        except ObjectDoesNotExist:
            return HttpResponse("The team not yet enrolled first form a team", content_type="text/plain")

        team=Team.objects.get(team_id=team_id)
        team.team_size +=1

        eventdetails=EventDetails.objects.filter(qr_code=qr_code,team_id=team_id)

        if isEligible(eventdetails.event_id,qr_code):

            eventdetails.update(status_choice="RUNNING",team_id =team_id)
            eventdetails.save()

            profile = Profile.objects.get(qr_code=qr_code)

            json_data = serializers.serialize('json', [eventdetail, profile])
            return HttpResponse(json_data, content_type="application/json")

        else:
            return HttpResponse("Not yet paid for the game", content_type="text/plain")

    else:
        message='Not a Valid Request'

    return HttpResponse(message,content_type="text/plain")


#Ends the game adding score and updating participated
# URL events/endgame
@csrf_protect
def endGame(request):

    Message="Error in calling the method"

    if request.method=='POST':

        team_id=EventDetails.objects.get(team_id='team_id')
        event=Event.objects.get('event_id')
        #this has to be changed the proper condition in if
        if participation_points:

             score=event.participation_points
        else:
            score=event.merit_points

        queryset=EventDetails.objects.filter(team_id=team_id)

        for player in queryset:

            player.status_choice = 'PLAYED'
            qr_code=player.qr_code
            profile=Profile.objects.get(qr_code=qr_code)
            profile.total_points +=score
            profile.save()

    else:
        message = 'Not a Valid Request'

    return HttpResponse(message, content_type="text/plain")









