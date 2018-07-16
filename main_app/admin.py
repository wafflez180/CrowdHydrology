from django.contrib import admin
from main_app.models import SMSContribution, InvalidSMSContribution, Station, Sponsor

# Register your models here.

admin.site.register(SMSContribution)
admin.site.register(InvalidSMSContribution)
admin.site.register(Station)
admin.site.register(Sponsor)
