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

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
import ast
#-----------------------------------------------------------------------------------

#PAYMENT DESK



@csrf_exempt
def cost(request):
    qr_code = request.POST.get("qr_code")
    pro = Profile.objects.get(qr_code=qr_code)
    no_of_events_for_pro = EventDetails.objects.filter(qr_code=pro).__len__()

    if no_of_events_for_pro < 3:
        pro.cost=no_of_events_for_pro*40
    elif (no_of_events_for_pro>=3 & no_of_events_for_pro<6):
        ((no_of_events_for_pro // 3) * 100) + ((no_of_events_for_pro % 3) * 40)

    elif (no_of_events_for_pro>=6):
        pro.cost=200

    pro.save()

    return pro.cost




# URL register/fetch
@csrf_exempt
def getUserEvent(request):

    message='Error'
    if request.method == 'POST':
        try:
            print(request.POST)
            qr_code=request.POST.get("qr_code")
            print(qr_code)

            pro = Profile.objects.get(qr_code=qr_code)
            print(pro.user)
            print(pro.qr_code)

        except ObjectDoesNotExist:
            return HttpResponse("QR Code is not valid",content_type="text/plain")

        #sending all registered events both paid and not paid , we disable register for the events paid in app

        kp=pro.pk
        print(kp)
        queryset=EventDetails.objects.filter(qr_code=kp)

        # print(queryset)
        #
        #
        # if not queryset:
        #     return HttpResponse("No events registered",content_type="text/plain")
        #

        json_data = serializers.serialize('json',queryset)
        return HttpResponse(json_data, content_type="application/json")


    else:
        message="wrong method called"
        return HttpResponse(message,content_type="text/plain")






# URL register/push
@csrf_exempt
def modifyRegistrationsAndParticipations(request):
    message="Error"
    if request.method=='POST':
        qr_code = request.POST.get("qr_code")

        print(qr_code)
        print("this is")
        #queryset =EventDetails.objects.filter(qr_code=profile)

        #if the jason format has [{qid:qid},{events:[(event ids)]}]

        eventlist=request.POST.get('events')


        print(eventlist)

      #  event_dic = {"'eid1'":'eid1',"'eid2'":'eid2',"'eid3'":'eid3',"'eid4'":'eid4',"'eid5'":'eid5',"'eid6'":'eid6',"'eid7'":'eid7',"'eid8'":'eid8',"'eid9'":'eid9',"'eid10'":'eid10',"'eid11'":'eid11',"'eid12'":'eid12'}
        eventlist  = eventlist.split(" ")
        eventlist = [ x.strip("[") for x in eventlist]
        eventlist = [ x.strip(",") for x in eventlist]
        eventlist = [ x.strip("]") for x in eventlist]

        pro=Profile.objects.get(qr_code=qr_code)


        for event in eventlist:

            print(event)
            try:
                obj=EventDetails.objects.get(qr_code=pro,event_id=event)
                obj.amount_paid = True
                obj.payment_mode = 'OFF'
                obj.save()
            except ObjectDoesNotExist:
                newEvent = Event.objects.get(event_id=event)
                newEvent=EventDetails(status_choice='WAITING',event_id=newEvent,team_id='none',qr_code=pro,amount_paid=True,payment_mode='OFF')
                newEvent.save()





        message="Successfully Updated"

        return HttpResponse(message, content_type="text/plain")
    else:
        message = 'Invalid Request'

    return HttpResponse(message, content_type="text/plain")


#---------------------------------------------------------------------------------------------------------
# EVENT ORGANISER

#For checking the user is playing for first time or is he a valid player

@csrf_exempt
def validateGame(event_id,qr_code):
    try:
        profile=Profile.objects.get(qr_code=qr_code)

    except:
        return False
    try:
        eventdetails = EventDetails.objects.get(qr_code=profile,event_id=event_id)
    except ObjectDoesNotExist:
            return False



    if ((eventdetails.amount_paid==True) & (eventdetails.status_choice!="PLAYED")):

        return True


    else:
        return False


#For starting a new game with single qr_code
#URL events/newgame

@csrf_exempt
def newGame(request):

    Message='Error'

    if request.method=='POST':
        event_id=request.POST.get('event_id')
        qr_code=request.POST.get('qr_code')
        
        if '.com' in qr_code:
            qr_code = qr_code[:-10]
        print(event_id)
        if validateGame(event_id,qr_code):


            team_id=generateTeamId(event_id,qr_code)
            print(team_id)
            print(event_id)
            pro=Profile.objects.get(qr_code=qr_code)
            eventinstance=Event.objects.get(event_id=event_id)
            eventdetail=EventDetails.objects.get(qr_code=pro,event_id=eventinstance)
            print(eventdetail.status_choice)
            eventdetail.status_choice='R'
            eventdetail.team_id =team_id
            eventdetail.save()
            print( eventdetail.team_id)


            json_data=serializers.serialize('json',[eventdetail,pro.user])
            return HttpResponse(json_data,content_type="application/json")

        else :
            message= 'User is not Allowed to Play'
    else:
        message='Not a Valid Request'

    return HttpResponse(message,content_type="text/plain")










#Generates unique GID which doesn't occur in the data base
@csrf_exempt
def generateTeamId(event_id,qr_code):

    '''event=Event.objects.get(event_id=event_id)
    event.event_count=event.event_count+1
    event.save()'''
    print("hi im here")
    print(qr_code)
    print(type(qr_code))
    return "%s%s%s" %(event_id,event_id,qr_code)


#Takes Existing Gid and adds Players
# URL @ events/addplayer
@csrf_exempt
def appendPlayers(request):

    Message="Error in requesting method"

    if request.method=='POST':

        qr_code=request.POST.get('qr_code')
        team_id=request.POST.get('team_id')
        event_id=request.POST.get('event_id')
        
        if '.com' in qr_code:
            qr_code = qr_code[:-10]

        try:
            pro=Profile.objects.get(qr_code=qr_code)
        except ObjectDoesNotExist:

            return HttpResponse("Invalid QR code",content_type="text/plain")


       # eventdetails=EventDetails.objects.filter(qr_code=pro,event_id=event_id)

        if validateGame(event_id,qr_code):
            eventdetails = EventDetails.objects.get(qr_code=pro,event_id=event_id)
            eventdetails.status_choice="RUNNING"
            eventdetails.team_id =team_id
            eventdetails.save()

            profile = Profile.objects.get(qr_code=qr_code)

            json_data = serializers.serialize('json', [eventdetails.qr_code, profile.user])
            return HttpResponse(json_data, content_type="application/json")

        else:
            return HttpResponse("Not yet paid for the game", content_type="text/plain")

    else:
        message='Not a Valid Request'

    return HttpResponse(message,content_type="text/plain")


#Ends the game adding score and updating participated
# URL events/endgame
@csrf_exempt
def endGame(request):

    Message="Error in calling the method"

    if request.method=='POST':

        team_id= request.POST.get('team_id')

        #event=Event.objects.get('event_id')
        #this has to be changed the proper condition in if


        score=request.POST.get('score')

        queryset=EventDetails.objects.filter(team_id=team_id)
        print(len(queryset))

        for player in queryset:

            player.score = score
            player.status_choice = 'PLAYED'
            player.save()
            qr_code=player.qr_code.qr_code
            profile=Profile.objects.get(qr_code=qr_code)
            profile.total_points = int(profile.total_points)+int(score)
            profile.save()

        return HttpResponse("Successfully Submitted!")

    else:
        message = 'Not a Valid Request'

    return HttpResponse(message, content_type="text/plain")









