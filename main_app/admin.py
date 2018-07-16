from django.contrib import admin
from main_app.models import SMSContribution, InvalidSMSContribution, Station, Sponsor

# Register your models here.

class SMSContributionAdmin(admin.ModelAdmin):
    search_fields = ['contributor_id', 'station', 'water_height', 'temperature', 'date_received']
    list_filter = ['station']
    list_display = ['contributor_id', 'water_height', 'temperature', 'station', 'date_received']

class InvalidSMSContributionAdmin(admin.ModelAdmin):
    search_fields = ['contributor_id', 'message_body']
    list_display = ['contributor_id', 'message_body', 'date_received']

class StationAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'state']
    list_filter = ['status', 'water_body_type', 'state']
    list_display = ['id', 'name', 'state', 'water_body_type', 'status', 'date_added']
    #list_editable = ['status']

class SponsorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

admin.site.register(SMSContribution, SMSContributionAdmin)
admin.site.register(InvalidSMSContribution, InvalidSMSContributionAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Sponsor, SponsorAdmin)
