from django.db import models
from django.contrib.auth.models import User

class Organizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Profile(models.Model):
    YEAR_CHOICES = (('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'))

    IT = 'IT'
    EEE = 'EEE'
    ECE = 'ECE'
    CIVIL = 'CIVIL'
    CSE = 'CSE'
    MECH = 'MECH'
    CHEMICAL = 'CHEMICAL'
    EIE = 'EIE'
    TEXTILE = 'TEXTILE'

    BRANCH_CHOICES = ((IT, 'INFORMATION TECHNOLOGY'), (EEE, 'ELECTRICAL AND ELECTRONICS ENGINEERING'),
                      (ECE, 'ELECTRONICS AND COMMUNICATION ENGINEERING'), (CIVIL, 'CIVIL'), (CSE, 'COMPUTER SCIENCE'),
                      (MECH, 'MECHANICAL'), (CHEMICAL, 'CHEMICAL'),
                      (EIE, 'ELECTRONICS AND INSTRUMENTATION ENGINEERING'), (TEXTILE, 'TEXTILE'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, default="1602-70-700-777")
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, default="I")
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, default="IT")
    college = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10, default="NoNumber")
    qr_code = models.CharField(max_length=30,default=0)
    total_points = models.IntegerField(default=0)
    cost=models.IntegerField(default=0)
class Event(models.Model):
    event_id = models.CharField(max_length=5, default="NULL", primary_key=True)
    event_name = models.CharField(max_length=50)
    team_size = models.IntegerField(default=1)
    event_organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    event_cost = models.IntegerField(default=0)
    participation_points=models.IntegerField(default=0)
    merit_points=models.IntegerField(default=0)

    def __str__(self):
        return self.event_id


class EventDetails(models.Model):
    WAITING = 'W'
    RUNNING = 'R'
    PLAYED = 'P'

    STATUS_CHOICES = ((RUNNING, 'RUNNING'), (PLAYED, 'PLAYED'), (WAITING, 'WAITING'))
    ONLINE = 'ON'
    OFFLINE = 'OFF'
    NONE = 'NONE'

    status_choice = models.CharField(max_length=8, choices=STATUS_CHOICES,default="WAITING")
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE, max_length=5)
    team_id = models.CharField(max_length=20)
    qr_code = models.ForeignKey('Profile', on_delete=models.CASCADE, max_length=50)
    amount_paid = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=10, choices=STATUS_CHOICES,default='OFF')




class Team(models.Model):

    team_id = models.CharField(max_length=20, unique=True)
    team_size = models.IntegerField(default=1)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE, max_length=5)

    def __str__(self):
        return self.event_id



class Otpgenerator(models.Model):
    mailid = models.CharField(max_length=40,primary_key=True)
    otp = models.IntegerField()


class Payments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=32)
    payment_status = models.CharField(max_length=30)
    payment_request_id = models.CharField(max_length=32)
    eventname=models.TextField(null=True, blank=True)

    def __str__(self):
        return ','.join([self.user.email, self.payment_id])




