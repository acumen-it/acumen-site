from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#team-model
class Team(models.Model):
    NGO_APPLICATIONS = 'NGO APPLICATIONS'
    XR = 'XR - AR/MR/VR'
    SMART_CITY = 'SMART CITY'
    WOMEN_SAFETY = 'WOMEN SAFETY'
    EDUTAINMENT = 'EDUTAINMENT'
    IAPPS = 'INTELLIGENTS APPLICATIONS'
    STARTUP_IDEAS = 'STARTUP IDEAS'

    THEME_CHOICES = (
                        (NGO_APPLICATIONS, 'NGO APPLICATIONS'), 
                        (XR, 'XR - AR/MR/VR'), 
                        (SMART_CITY, 'SMART CITY'), 
                        (WOMEN_SAFETY, 'WOMEN SAFETY'), 
                        (EDUTAINMENT, 'EDUTAINMENT'), 
                        (IAPPS, 'INTELLIGENTS APPLICATIONS'),
                        (STARTUP_IDEAS, 'STARTUP IDEAS'),
                    )
    
    name = models.CharField(max_length=128, unique=True)
    team_lead = models.CharField(max_length=1024, default=None)
    project_link = models.CharField(max_length=1024, blank=True)
    theme = models.CharField(max_length=64, choices=THEME_CHOICES)

    def __str__(self):
        return ','.join([self.name])

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=32)
    payment_status = models.CharField(max_length=30)
    payment_request_id = models.CharField(max_length=32)

    def __str__(self):
        return ','.join([self.user.email, self.payment_id])

#participant-model
class Participant(models.Model):
    #name, college, year, branch, email, contactno
    I = 'I'
    II = 'II'
    III = 'III'
    IV = 'IV'
    
    YEAR_CHOICES=((I,'I'),(II,'II'),(III,'III'),(IV,'IV'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=128)
    year = models.CharField(max_length = 3, choices = YEAR_CHOICES, default = "I",blank=True)
    branch = models.CharField(max_length=128,blank=True)
    contact = models.CharField(max_length=15)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return ','.join([self.user.email, self.contact])
        