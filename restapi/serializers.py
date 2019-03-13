from rest_framework import serializers
from acusite.models import Profile,Event,EventDetails,Team

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields=("qr_code","user","roll_number")


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model=Event
        fields=("event_id","event_name","team_size","event_cost")



class EventDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model=EventDetails
        fields=("event_id","status_choice")

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team

class PaymentDeskSerializer(serializers.ModelSerializer):

    profile=ProfileSerializer(many=True,read_only=True)
    event=EventSerializer(many=True,read_only=True)
    event_details=EventDetailsSerializer(many=True,read_only=True)

    class Meta:
        fields=("profile","event","event_details")








