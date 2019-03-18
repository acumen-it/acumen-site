from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
@admin.register(Participant)
class ParticipantAdmin(ImportExportModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    pass
