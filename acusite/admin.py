from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Profile,Event,EventDetails,Organizer,Team,Otpgenerator

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass

@admin.register(Organizer)
class OrganizerAdmin(ImportExportModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    pass

@admin.register(EventDetails)
class EventDetailsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Otpgenerator)
class OtpgeneratorAdmin(ImportExportModelAdmin):
    pass


# Register your models here.
